from user import serializers as user_serializer
import os
import logging
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from user import models as user_models

from rest_framework import status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import views, response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from permission.mixins import Auth, Public
logger = logging.getLogger(__name__)

User = get_user_model()


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
            user = User.objects.get(email=email)
        except User.DoesNotExist:
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

class LogoutView(Auth,views.APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return response.Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return response.Response({"error": "Invalid token"}, status=400)
