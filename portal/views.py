from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import (response, status)

from django.http import FileResponse, JsonResponse, Http404
from django.core.mail import send_mail
from django.template.loader import render_to_string

from user_profile import models as userProfileModels

import os
import logging

logger = logging.getLogger(__name__)

class VideoPortalView(APIView):
    def get(self, request, *args, **kwargs):
        video_path = os.path.join('portal', 'templates', 'videos', 'video_cmr_v2.mp4')
        
        try:
            # Verifica se o arquivo existe e tenta abri-lo
            if not os.path.exists(video_path):
                raise Http404("Arquivo não encontrado")

            return FileResponse(open(video_path, 'rb'), content_type='video/mp4')
        
        except FileNotFoundError:
            # Caso o arquivo não seja encontrado
            return JsonResponse({'error': 'Arquivo não encontrado'}, status=404)
        
        except OSError as e:
            # Para qualquer outro erro relacionado ao sistema de arquivos
            return JsonResponse({'error': f'Erro ao acessar o arquivo: {str(e)}'}, status=500)

class ContatoView(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        last_name = request.data.get('surname')
        email_sender = request.data.get('email')
        phone = request.data.get('phone'),
        message = request.data.get('message')

        subject = 'Contato via fale conosco'

        context = {
            'name': name,
            'last_name': last_name,
            'phone': phone,
            'message': message
        }

        html_message = render_to_string('email/contato.html', context)


        try:
            send_mail(subject, message='', from_email=email_sender, recipient_list=['valdean.junior@hex360.com.br', 'marcos.silva@hex360.com.br'], html_message=html_message)
            return response.Response({"detail": "Email enviado com sucesso."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CadastroView(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        email = request.data.get('email')
        department = request.data.get('department')
        registration = request.data.get('registration')
        coordinator_name = request.data.get('coordinatorName')
        coordinator_email = request.data.get('coordinatorEmail')
        coordinator_department = request.data.get('coordinatorDepartment')
        siape_registration = request.data.get('siapeRegistration')
        attachment = request.FILES.get('attachment') 

        if attachment:
            upload_dir = os.path.dirname(os.path.join('media/attachments/', attachment.name))
    
            # Verifica se o diretório de upload existe; se não, cria-o
            if not os.path.exists(upload_dir):
                logger.info(f"Criando o diretório de upload: {upload_dir}")
                os.makedirs(upload_dir)
            else:
                logger.info(f"O diretório de upload já existe: {upload_dir}")

            upload_path = os.path.join('media/attachments/', attachment.name)
            logger.debug(f"Upload path: {upload_path}")

            # Verifica se o diretório de upload existe
            if not os.path.exists(os.path.dirname(upload_path)):
                logger.error(f"O caminho de upload {os.path.dirname(upload_path)} não existe.")
            else:
                logger.info(f"Upload do arquivo será realizado em {upload_path}.")
        else:
            logger.warning("Nenhum arquivo de anexo foi fornecido.")

        cadastro = userProfileModels.AccessRequest.objects.create(
            name=name,
            email=email,
            department=department,
            user_siape_registration=registration,
            coordinator_name=coordinator_name,
            coordinator_email=coordinator_email,
            coordinator_department=coordinator_department,
            coordinator_siape_registration=siape_registration,
            attachment=attachment
        )
        
        return response.Response({'message': 'Cadastro realizado com sucesso.'}, status=status.HTTP_201_CREATED)
