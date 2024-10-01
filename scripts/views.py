from django.shortcuts import render
import xml.etree.ElementTree as ET
from support import models
from datetime import datetime

from ldap3 import Server, Connection, SUBTREE

from django.contrib.auth.models import User

from django.conf import settings

import requests
import json
import untangle
import logging

logger = logging.getLogger(__name__)

# Create your views here
class JobSccon():
    
    def get_queryset(self):
        return models.TmsLayer.objects.all().order_by('-date')

    def get_last_tms(self, *args, **kwargs):
        """ function to get all last TMS registers in databsase """

        queryset = self.get_queryset()
        tms_data = []
        for data in queryset:
            info = {'date': data.date, 'url_tms': data.url_tms}
            tms_data.append(info)
        return tms_data
        

    def run_sccon(self, *args, **kwargs):
        """ Script function to get all links and identifiers from sccon  based on actual year """

        req_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        url = 'https://plataforma-pf.sccon.com.br/gama-api/auth/token?password=CMR@Funai2023&username=hex@funai.gov.br'
        req = requests.get(url, headers=req_headers)

        res_json = json.loads(req.text)

        access_token = res_json['access_token']

        req_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Authorization': f'Bearer {access_token}'}
        url = 'https://plataforma-pf.sccon.com.br/gama-api/users-planet/users/609c9c0f-5244-4714-b5cf-ac3a9078fe54'
        req = requests.get(url, headers=req_headers)

        res_json = json.loads(req.text)

        gsa_json = res_json['geoserviceAccesses']

        wmts_json = gsa_json[0]

        req_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        url = wmts_json['link']
        req = requests.get(url, headers=req_headers)

        old_tiling = '{TileMatrix}/{TileCol}/{TileRow}'
        new_tiling = '{z}/{x}/{y}'

        filtered = req.text.replace(old_tiling, new_tiling)
        res_xml = untangle.parse(filtered)

        data = {}

        for layer in res_xml.Capabilities.Contents.Layer:
            inner_data = []
            title = layer.ows_Title.cdata
            identifier = layer.ows_Identifier.cdata
            link = layer.ResourceURL['template']
            
            if identifier.startswith('global_monthly'):
                ano = identifier[15:19]
                mes = identifier[20:22]

                if ano in data:
                    inner_data = data[ano]
                info = {'title' : title, 'identifier' : identifier, 'mes' : mes, 'link' : link}
                inner_data.append(info)
                data[ano] = inner_data
                planet_json = json.dumps(data)
                
        filtrado = json.loads(planet_json)

        identifiers = []
        links = []
        sccon_data= []

        tms_data = self.get_last_tms()
        dates_tms = [item['date'] for item in tms_data]
        
        if dates_tms:
            max_date = max(dates_tms)
            year_search = str(max_date.year)
        else:
            print("No dates available")
            return

        for i in filtrado[year_search]:
            identifier = i['identifier']
            link = i['link']
            # print(f"Identificador: {identifier}")
            # print(f"link {link}"+'\n')
            identifiers.append(identifier)
            links.append(link)

            info = {'identifier': identifier, 'link': link}
            sccon_data.append(info)

        return sccon_data
    
    def get_unregistered_links(self):
        """ function to get all unregistered data from sccon  """

        tms_data = self.get_last_tms()
        sccon_data = self.run_sccon()

        dates_tms = [item['date'] for item in tms_data]
        info_scoon = [item['identifier'] for item in sccon_data]
        
        if info_scoon: 
            try:
                len_sccon = len(info_scoon)
                last_scoon = info_scoon[len_sccon-1]
                actual_year = datetime.now().year
                month_last_sccon = str(last_scoon.replace(f'global_monthly_{actual_year}_', '').replace('_mosaic', ''))
                month_last_sccon_number = int(month_last_sccon)

                if dates_tms:
                    max_date = max(dates_tms)
                    max_date_number = int(max_date.month) 
                    b = month_last_sccon_number - max_date_number

                    print(f"Month number of last sccon registration: {month_last_sccon_number}")
                    print(f"Month number of last CMR registration: {max_date.month}")
                    print(f"Number of months not recorded: {b}")

                    if b >= 0:
                        last_b_records = sccon_data[-b:]
                        print(f'Data to be recorded: {last_b_records}')
                        return last_b_records, month_last_sccon_number
                    else:
                        print("No records to display based on the calculated difference.")
                        return None

            except Exception as e:
                print(f'Error: {e}')
                return None

    def get_layers_group(self, *args, **kwargs):
        """ function to get all data from layers group and if no has data for this year register a new  """

        actual_year = datetime.now().year
        try:
            queryset = models.LayersGroup.objects.get(name=f'Mosaico Planet {actual_year}')
            if queryset:
                print(f"ID: {queryset.pk}")
                print(f"Name: {queryset.name}")
                print(f"Order: {queryset.order}")
                print(f"Category Groups: {queryset.category_groups}")
                return queryset
        except models.LayersGroup.DoesNotExist:
            last_layers_group = models.LayersGroup.objects.latest('order')
            new_order = int(last_layers_group.order)+1
            c_groups = models.CategoryLayersGroup.objects.get(pk=3)

            create_layer_group = models.LayersGroup(
                name=f'Mosaico Planet {actual_year}',
                order=new_order,
                category_groups=c_groups
            )
            create_layer_group.save()
            print("dados salvos com sucesso!")
            return create_layer_group
        
    def create_new_layer(self, identifier, *args, **kwargs):
        """ function to get all data from layers and if no has data for this month register a new  """
        
        actual_year = datetime.now().year
        month_names_pt = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        layer_group = self.get_layers_group()
        l_group_instance = models.LayersGroup.objects.get(pk=layer_group.pk)

        identifier_replace = str(identifier.replace(f'global_monthly_{actual_year}_', '').replace('_mosaic', ''))
        month_name = month_names_pt[int(identifier_replace) - 1]
        layer_name = f'{identifier_replace} - {month_name}'

        layer, created = models.Layer.objects.get_or_create(
            name=layer_name,
            defaults={
                'layer_type': 'tms',
                'layers_group': l_group_instance,
            }
        )

        if created:
            print(f'Layer criado: {layer}')
        else:
            print(f'Layer já existe: {layer}')
        
        return layer
   
    def create_tms(self, *args, **kwargs):
        """ Function to create a new TMS register base on non registered data geted by sccon """

        result = self.get_unregistered_links()

        if result is None:
            print("No records to display based on the calculated difference.")
            return

        last_b_records, month_last_sccon_number = result

        month_names_pt = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        for item in last_b_records:
            actual_year = datetime.now().year
            identifier_replace = str(item['identifier'].replace(f'global_monthly_{actual_year}_', '').replace('_mosaic', ''))
            month_name = month_names_pt[int(identifier_replace) - 1]
            search_name = f'{identifier_replace} - {month_name}'

            try:
                get_layer_instance = models.Layer.objects.get(name=search_name)
            except models.Layer.DoesNotExist:
                get_layer_instance = self.create_new_layer(item['identifier'])

            try:
                tms_register = models.TmsLayer(
                    url_tms=item['link'],
                    date=datetime.now().date(),
                    max_native_zoom=9,
                    layer=get_layer_instance
                )
                tms_register.save()
                print(f"TmsLayer registrado com sucesso: {tms_register}")

            except Exception as e:
                print(f"Erro ao registrar TmsLayer: {e}")

class JobMonitoringAd:
    
    def sincronize_with_django(self):
        ldap_uri = '10.0.0.1'
        ldap_port = 389
        base_dn = settings.LDAP_BASE_DN
        use_tls = False              

        sAMAccountName = 'hex'
        domain = 'FUNAI'
        ldap_password = settings.LDAP_PASS

        ldap_connection = None

        try:
            ldap_bind_dn = f'{domain}\\{sAMAccountName}'
            server = Server(ldap_uri, port=ldap_port, use_ssl=use_tls)
            ldap_connection = Connection(server, user=ldap_bind_dn, password=ldap_password, auto_bind=True)

            logger.debug("LDAP connection established successfully.")

            ldap_connection.search(
                search_base=base_dn,
                search_filter='(&(objectClass=*))',
                search_scope=SUBTREE,
                attributes=['sAMAccountName', 'mail']
            )

            django_users = {user.username: user for user in User.objects.all()}
            ad_usernames = []

            for entry in ldap_connection.entries:
                user_mail = entry.mail.value if 'mail' in entry else None
                user_samaccountname = entry.sAMAccountName.value if 'sAMAccountName' in entry else None

                if not user_samaccountname or not user_mail:
                    logger.debug(f"Skipping entry due to missing sAMAccountName or mail: {entry}")
                    continue

                ad_usernames.append(user_samaccountname)

                parts = user_samaccountname.split('.')
                first_name = parts[0] if len(parts) > 0 else ""
                last_name = parts[1] if len(parts) > 1 else ""

                user_defaults = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': user_mail,
                }

                if user_samaccountname in django_users:
                    user = django_users[user_samaccountname]
                    changes_needed = any(
                        getattr(user, field) != value
                        for field, value in user_defaults.items()
                    )
                    if changes_needed:
                        for field, value in user_defaults.items():
                            setattr(user, field, value)
                        user.save()
                        logger.debug(f"Updated user: {user.username}, email: {user.email}")
                    else:
                        logger.debug(f"No changes needed for user: {user.username}")
                else:
                    user = User.objects.create(username=user_samaccountname, **user_defaults)
                    logger.debug(f"Created user: {user.username}, email: {user.email}")
            
        except Exception as e:
            logger.error(f"Error: {e}")

        finally:
            if ldap_connection:
                ldap_connection.unbind()        
                #           python manage.py monitoring_ad_users