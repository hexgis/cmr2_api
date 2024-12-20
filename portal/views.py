from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import (response, status)
from rest_framework.permissions import AllowAny

from django.http import FileResponse, JsonResponse, Http404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from user_profile import models as userProfileModels

import os
import logging

logger = logging.getLogger(__name__)

class VideoView(APIView):
    """Serve a video file from the media directory."""
    permission_classes = [AllowAny]
    
    def get_authenticators(self):
        if hasattr(self.request, '_disable_jwt') and self.request._disable_jwt:
            return []
        return super().get_authenticators()

    def get(self, request, *args, **kwargs):
        """Serve the video file or return an error if not found.

        Args:
            request (rest_framework.request.Request): The HTTP request object.

        Returns:
            FileResponse: If the video file exists.
            JsonResponse: If the file is not found or there's an access error.
        """
        video_path = os.path.join(settings.VIDEO_TEMPLATE_DIR, 'video_cmr_v2.mp4')

        try:
            # Open the video file and return it as a FileResponse
            return FileResponse(open(video_path, 'rb'), content_type='video/mp4')
        except FileNotFoundError:
            return JsonResponse({'error': 'Arquivo não encontrado'}, status=404)
        except OSError as e:
            return JsonResponse({'error': f'Erro ao acessar o arquivo: {str(e)}'}, status=500)


class ContactView(APIView):
    """Handles contact form submissions and sends an email with the details."""
    permission_classes = [AllowAny]
    
    def get_authenticators(self):
        if hasattr(self.request, '_disable_jwt') and self.request._disable_jwt:
            return []
        return super().get_authenticators()

    def post(self, request, *args, **kwargs):
        """Process the contact form submission and send an email.

        Args:
            request (rest_framework.request.Request): The HTTP request object containing form data.

        Returns:
            Response: Success message if email is sent, or error message if something goes wrong.
        """
        # Email subject and context for the email template.
        subject = 'Contato via fale conosco'
        context = {
            'name': request.data.get('name'),
            'last_name': request.data.get('surname'),
            'phone': request.data.get('phone'),
            'message': request.data.get('message')
        }
        template_path = os.path.join(settings.EMAIL_TEMPLATES_DIR, 'contato.html')
        # Render the email message using the context.
        html_message = render_to_string(template_path, context)

        try:
            # Send the email to specified recipients.
            send_mail(
                subject, 
                message='', 
                from_email=request.data.get('email'), 
                recipient_list=settings.RECIPIENT_LIST_EMAIL_DEV, # 🦆 Change to admin emails.
                html_message=html_message
            )
            return response.Response({"detail": "Email enviado com sucesso."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

class RegisterView(APIView):
    """Handles registration requests and sends an email with the details."""
    permission_classes = [AllowAny]
    
    def get_authenticators(self):
        if hasattr(self.request, '_disable_jwt') and self.request._disable_jwt:
            return []
        return super().get_authenticators()

    def post(self, request, *args, **kwargs):
        """Process registration data and handle file uploads.

        Args:
            request (rest_framework.request.Request): The HTTP request object containing form data and file upload.

        Returns:
            Response: Success message if registration and email sending succeed, or error message if something goes wrong.
        """
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
            attachment_path = os.path.join(settings.MEDIA_ROOT)
            upload_path = self._handle_upload_path(f'{attachment_path}attachments/', attachment.name)
            logger.debug(f"Upload path: {upload_path}")
        else:
            logger.warning("Nenhum arquivo de anexo foi fornecido.")
        
        try:
            # Create a new record in the database.
            userProfileModels.AccessRequest.objects.create(
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
            
            # Prepare and send the notification email.
            context = {'name': name}
            subject = 'Pedido de acesso ao CMR'
            template_path = os.path.join(settings.EMAIL_TEMPLATES_DIR, 'solicitacao_de_acesso.html')
            html_message = render_to_string(template_path, context)

            try:
                send_mail(
                    subject,
                    message='', 
                    from_email="cmr@funai.gov.br",
                    recipient_list= settings.RECIPIENT_LIST_EMAIL_DEV, # 🦆 Change to admin emails.
                    html_message=html_message
                )
                return response.Response({"detail": "Pedido enviado com sucesso!"}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error sending email: {str(e)}")
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Error creating database record: {str(e)}")
            return JsonResponse({'error': 'Error creating database record.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def _handle_upload_path(self, base_dir, filename):
        """Helper method to handle file upload directory creation."""
        upload_dir = os.path.dirname(os.path.join(base_dir, filename))
        if not os.path.exists(upload_dir):
            logger.info(f"Criando o diretório de upload: {upload_dir}")
            os.makedirs(upload_dir)
        else:
            logger.info(f"O diretório de upload já existe: {upload_dir}")
        return os.path.join(base_dir, filename)
