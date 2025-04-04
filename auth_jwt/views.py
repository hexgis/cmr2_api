import os
import logging
import pytz
import requests

from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta

from user_agents import parse as parse_user_agent
from user import serializers as user_serializer

from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from user import models as user_models
from django.utils.translation import gettext_lazy as _

from rest_framework import status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import views, response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist
from permission.mixins import Auth, Public
from dashboard import models as dashModels

from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import (
    response,
    permissions,
    views,
    status,
    serializers,
    generics
)

User = get_user_model()
logger = logging.getLogger(__name__)


class ChangePassword(Auth, views.APIView):
    """View to change User password."""

    def post(self, request, *args, **kwargs):
        """Post method to change User password for received data.

        Args:
            request (DRF request): user request with old and new
                password data.

        Returns:
            response: invalid or correct response for new password.
        """

        old_password = request.data['oldPassword']
        new_password1 = request.data['newPassword1']
        user = request.user

        if user.check_password(old_password):
            user.set_password(new_password1)
            user.save()

            refresh = RefreshToken.for_user(user)

            return response.Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            message = 'Invalid password.'

        error_response = {'message': message}
        return response.Response(error_response, status=400)


class ResetPassword(Public, views.APIView):
    """Endpoint to handle password reset requests."""

    serializer_class = user_serializer.PasswordResetRequestSerializer

    def get_authenticators(self):
        """
        Desabilita autenticação JWT se for uma rota pública.
        """
        if getattr(self.request, '_disable_jwt', False):
            return []
        return super().get_authenticators()

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to reset a user's password.
        """
        # Validação do payload
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Restringe a recuperação de senha para e-mails '@funai.gov.br'
        if email.endswith('@funai.gov.br'):
            return Response({
                "detail": (
                    "Usuários FUNAI não podem alterar o e-mail através do CMR. "
                    "Para recuperar sua senha, por favor, entre em contato com o setor de TI da sua instituição."
                )
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se existe usuário com o e-mail fornecido
        try:
            user = get_user_model().objects.get(email=email)
        except ObjectDoesNotExist:
            return Response(
                {"detail": "User with this email does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # (Opcional) Verifica se o usuário está ativo
        if not user.is_active:
            return Response(
                {"detail": "Inactive user. Please contact support."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cria o código de reset e envia o e-mail em uma única transação
        try:
            with transaction.atomic():
                # Remove códigos de reset anteriores para evitar duplicidade
                user_models.PasswordResetCode.objects.filter(
                    user=user).delete()

                # Cria novo código de reset com expiração de 15 minutos
                reset_code = user_models.PasswordResetCode.objects.create(
                    user=user,
                    expires_at=timezone.now() + timedelta(minutes=15)
                )

                # Monta link de redefinição usando a URL configurada
                reset_link = settings.RESET_PASSWORD_URL.format(
                    code=reset_code.code)

                # Prepara conteúdo do e-mail (template + contexto)
                context = {
                    'user': user,
                    'reset_link': reset_link,
                    'reset_code': reset_code.code,
                }
                template_path = os.path.join(
                    settings.EMAIL_TEMPLATES_DIR, 'password_reset.html')
                html_message = render_to_string(template_path, context)

                subject = 'Solicitação de Recuperação de Senha do CMR'
                from_email = settings.DEFAULT_FROM_EMAIL

                # Envia o e-mail de recuperação
                send_mail(
                    subject=subject,
                    message='',
                    from_email=from_email,
                    recipient_list=[email],
                    html_message=html_message
                )

        except Exception as e:
            # Loga a exceção para monitoramento
            logger.exception("Failed to send password reset email.")
            # Retorna uma resposta genérica de erro
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retorna mensagem de sucesso
        return Response(
            {"detail": "Password reset code sent."},
            status=status.HTTP_200_OK
        )


class LogoutView(Auth, views.APIView):
    """
    Handles user logout by blacklisting the provided refresh token.
    """

    def post(self, request):
        """
        Processes a POST request to log out the user.

        Expected request body:
        {
            "refresh": "string"  # The refresh token to be blacklisted
        }
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return response.Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return response.Response({"error": "Invalid token"}, status=400)


class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    Custom serializer to authenticate users and generate tokens.
    For @funai.gov.br users, authentication is done via AD only.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username_or_email = attrs.get('username')
        password = attrs.get('password')

        logger.debug(f"Validating credentials for: {username_or_email}")

        user = authenticate(
            request=self.context.get('request'),
            username_or_email=username_or_email,
            password=password
        )

        if not user:
            logger.debug(f"Authentication failed for {username_or_email}")
            raise serializers.ValidationError(
                _("Invalid username or password.")
            )

        logger.debug(
            f"User authenticated: {user.username} (email: {user.email})")

        # Gera o token manualmente
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        # Registra o acesso do usuário
        self._record_user_access(self.context.get('request'), user)

        return data

    def _record_user_access(self, request, user):
        """
        Registers the IP, location, etc., for the authenticated user in DashboardData.
        """
        public_user_ip = self.get_public_ip()
        user_location = self.get_location(public_user_ip)
        user_agent_info = self.get_user_agent_info(request)

        brasilia_tz = pytz.timezone('America/Sao_Paulo')
        current_date = timezone.now().astimezone(brasilia_tz)

        try:
            dashModels.DashboardData.objects.create(
                user=user,
                last_date_login=current_date,
                location=(
                    f"{user_location.get('city')}, "
                    f"{user_location.get('region')}, "
                    f"{user_location.get('country_name')}"
                ),
                ip=public_user_ip,
                browser=user_agent_info['browser'],
                type_device=user_agent_info['device'],
                latitude=user_location.get('latitude'),
                longitude=user_location.get('longitude'),
            )
            logger.info(f"Access recorded successfully for user {user}")
        except Exception as e:
            logger.error(f"Error recording user access: {e}")

    def get_public_ip(self):
        """
        Returns the user's public IP via ipify.
        """
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.warning(f"Could not fetch public IP: {e}")
            return "0.0.0.0"

    def get_location(self, ip):
        """
        Get the geographic location of the IP provided via ipapi.
        Returns dictionary with city, region, country_name, etc.
        """
        try:
            url = f'https://ipapi.co/{ip}/json/'
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'city': data.get('city'),
                    'region': data.get('region'),
                    'country_name': data.get('country_name'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude')
                }
            else:
                logger.warning(f"ipapi returned status {response.status_code}")
                return {'error': 'Unknown location'}
        except Exception as e:
            logger.error(f"Error fetching location from ipapi: {e}")
            return {'error': f'Error fetching location: {e}'}

    def get_user_agent_info(self, request):
        """
        Returns information about the user agent (browser and device type).
        """
        user_agent_str = request.META.get('HTTP_USER_AGENT', "")
        user_agent = parse_user_agent(user_agent_str)
        return {
            'browser': user_agent.browser.family,
            'device': 'mobile' if user_agent.is_mobile else
                      'tablet' if user_agent.is_tablet else 'PC'
        }
