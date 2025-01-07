import os
import logging

from django.conf import settings
from django.http import FileResponse, JsonResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework import response, status
from rest_framework.permissions import AllowAny
from rest_framework import generics, status, response

from user import models as userProfileModels
from permission import mixins

logger = logging.getLogger(__name__)


class VideoView(mixins.Public, APIView):
    """Serve a video file from the media directory."""

    def get(self, request, *args, **kwargs):
        """Serve the video file or return an error if not found."""
        video_path = os.path.join(
            settings.VIDEO_TEMPLATE_DIR,
            'video_cmr_v2.mp4'
        )
        try:
            return FileResponse(
                open(video_path, 'rb'),
                content_type='video/mp4'
            )
        except FileNotFoundError:
            return JsonResponse(
                {'error': 'Arquivo não encontrado'},
                status=404
            )
        except OSError as e:
            return JsonResponse(
                {'error': f'Erro ao acessar o arquivo: {str(e)}'},
                status=500
            )


class ContactView(mixins.Public, APIView):
    """Handles contact form submissions and sends an email with the details."""

    def post(self, request, *args, **kwargs):
        """Process the contact form submission and send an email."""
        subject = 'Contato via fale conosco'
        context = {
            'name': request.data.get('name'),
            'last_name': request.data.get('surname'),
            'phone': request.data.get('phone'),
            'message': request.data.get('message')
        }
        template_path = os.path.join(
            settings.EMAIL_TEMPLATES_DIR, 'contato.html')
        html_message = render_to_string(template_path, context)

        try:
            send_mail(
                subject,
                message='',
                from_email=request.data.get('email'),
                recipient_list=settings.RECIPIENT_LIST_EMAIL_DEV,
                html_message=html_message
            )
            return response.Response({"detail": "Email enviado com sucesso."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Erro ao enviar email: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
