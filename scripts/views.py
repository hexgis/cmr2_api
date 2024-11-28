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
    """
    Class responsible for managing the synchronization and creation of records 
    related to TMS layers from the SCCON platform.
    """

    def run_sccon(self, *args, **kwargs):
        """
        Executes a script to retrieve links and identifiers from the SCCON platform for the current year.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            list: A list of dictionaries containing information about TMS layers, such as year, month, and link.
        """
        # Omitted logic for brevity
        pass

    def get_unregistered_links(self):
        """
        Retrieves links from the SCCON platform that are not yet registered in the TmsLayer model.

        Returns:
            list: A list of dictionaries with information about unregistered TMS layers, 
            including year, month, and link.
        """
        # Omitted logic for brevity
        pass

    def check_or_create_layers_group_for_years(self):
        """
        Verifies the existence of LayersGroup records for the unregistered years found in SCCON data.
        Creates new LayersGroup records if they do not already exist.
        """
        # Omitted logic for brevity
        pass

    def check_or_create_layers(self):
        """
        Verifies the existence of Layer records for the unregistered months in SCCON data.
        Creates new Layer records if they do not already exist.
        """
        # Omitted logic for brevity
        pass

    def check_or_create_tms(self):
        """
        Verifies the existence of TmsLayer records for the unregistered links.
        Creates new TmsLayer records if they do not already exist.
        """
        # Omitted logic for brevity
        pass

    def verify_tms_layers(self):
        """
        Validates whether the TMS layers from the SCCON platform are already registered.
        If they are not, it triggers the creation of layers and TMS records.

        Prints:
            - Information about missing or already registered layers.
        """
        data = self.get_unregistered_links()

        if not data:
            print("No data was found in `data`.")
            return

        for item in data:
            year = item.get('ano')
            month = item.get('month')

            if not year or not month:
                print(f"Incomplete data: {item}")
                continue

            exists = supmodels.TmsLayer.objects.filter(ano=year, mes=month).exists()

            if not exists:
                print(f"Not registered: Year {year}, Month {month}")
                self.check_or_create_layers()
                self.check_or_create_tms()
            else:
                print(f"Year {year}, Month {month} has been registered.")

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