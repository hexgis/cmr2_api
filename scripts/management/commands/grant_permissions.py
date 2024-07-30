import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Send a POST request to a specific URL with given payload'

    def handle(self, *args, **kwargs):
        # Obtain the token
        auth_url = "http://localhost:8080/auth/obtain_token/"
        auth_payload = {
            "username": "root",
            "password": "hexgis2019"
        }
        auth_headers = {
            "Content-Type": "application/json"
        }

        auth_response = requests.post(auth_url, json=auth_payload, headers=auth_headers)
        
        if auth_response.status_code == 200:
            auth_data = auth_response.json()
            access_token = auth_data.get('access')
            if not access_token:
                self.stdout.write(self.style.ERROR('Access token not found in the response'))
                return
        else:
            self.stdout.write(self.style.ERROR(f'Failed to obtain token. Status code: {auth_response.status_code}'))
            return

        # Send the request with the obtained token
        url = "http://localhost:8080/authorization/grant-permissions-test/"
        payloads = [
            {
                "email": "root@hexgis.com",
                "role": "dev_master_admin",
                "permissions": []
            },
            # {
            #     "email": "joaofonseca@funai.com",
            #     "role": "funai_cmr_admin",
            #     "permissions": []
            # },
            # {
            #     "email": "andrezabarroso@funai.com",
            #     "role": "autenticado",
            #     "permissions": []
            # },
            # {
            #     "email": "user4@funai.com",
            #     "role": "funai_sede",
            #     "permissions": []
            # },
            # {
            #     "email": "user5@funai.com",
            #     "role": "funai_coordenacao_regional",
            #     "permissions": []
            # },
            # {
            #     "email": "user6@funai.com",
            #     "role": "funai_terra_indigena",
            #     "permissions": []
            # },
            # {
            #     "email": "user7@funai.com",
            #     "role": "fpe",
            #     "permissions": []
            # },
            # {
            #     "email": "user8@funai.com",
            #     "role": "outras_instituicoes",
            #     "permissions": []
            # },
            # {
            #     "email": "user9@funai.com",
            #     "role": "academico",
            #     "permissions": []
            # },
            # {
            #     "email": "user10@funai.com",
            #     "role": "cultural",
            #     "permissions": []
            # },
            # {
            #     "email": "user11@funai.com",
            #     "role": "nao_autenticado",
            #     "permissions": []
            # },

        ]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        for payload in payloads:
            response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS('Request sent successfully'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to send request. Status code: {response.status_code}'))