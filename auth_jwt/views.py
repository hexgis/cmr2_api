from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rolepermissions.roles import assign_role
from user_agents import parse as parse_user_agent

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
import requests 
import pytz
from datetime import timedelta
import uuid

from rest_framework import (
    response,
    permissions,
    views,
    status,
    serializers,
    generics
)

from user_profile import models as usrModels
from user_profile import serializers as usrSerializers
from dashboard import models as dashModels

User = get_user_model()

import logging

logger = logging.getLogger(__name__)



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizes the token obtain pair serializer to add additional functionalities.
    
    Attributes:
    - username_field: Specifies the field to be used for authentication (username).
    - email: An optional email field to be used in the authentication process.

    Methods:
    - get_public_ip: Retrieves the public IP address of the user.
    - get_location: Fetches the geographical location for a given IP address.
    - validate: Validates the authentication credentials and performs additional actions.
    """
    email = serializers.EmailField(required=False)

    def get_public_ip(self):
        """
        Retrieves the public IP address of the user by making a request to the ipify API.

        Returns:
        - str: The public IP address of the user.
        """
        response = requests.get('https://api.ipify.org').text
        return response
    
    def get_location(self, ip):
        """
        Fetches the geographical location for the given IP address using the ipapi API.

        Args:
        - ip (str): The IP address for which to fetch the location.

        Returns:
        - str: The location in the format "city, region, country" or an error message.
        """
        try:
            response = requests.get(f'https://ipapi.co/{ip}/json/')
            if response.status_code == 200:
                data = response.json()
                return f"{data.get('city')}, {data.get('region')}, {data.get('country_name')}"
            else:
                return "Unknown location"
        except Exception as e:
            return f"Error fetching location: {e}"
    
    def get_user_agent_info(self, request):
        user_agent_str = request.META.get('HTTP_USER_AGENT', " ")
        user_agent = parse_user_agent(user_agent_str)
        return {
            'browser': user_agent.browser.family,
            'device': 'mobile' if user_agent.is_mobile else 'tablet' if user_agent.is_tablet else 'PC'
        }
    

    def validate(self, attrs):
        """
        Validates the token obtain pair request and performs additional actions.

        Args:
        - attrs (dict): Dictionary of request attributes, including 'username' and 'password'.

        Returns:
        - dict: Validated data dictionary after authentication and additional actions.
        
        Raises:
        - serializers.ValidationError: If authentication fails or other errors occur.
        """
        
        # Retrieve username or email and password from request attributes
        request = self.context.get('request')
        username_or_email = attrs.get('username')
        password = attrs.get('password')

        # Attempt to authenticate the user using username
        user = authenticate(username=username_or_email, password=password)
        if not user:
            # If authentication fails, try to authenticate with email or username
            try:
                user = User.objects.get(email=username_or_email)
                if not user.check_password(password):
                    raise serializers.ValidationError(_('Wrong password.'))
            except User.DoesNotExist:
                try:
                    user = User.objects.get(username=username_or_email)
                    if not user.check_password(password):
                        raise serializers.ValidationError(_('Wrong password.'))
                except User.DoesNotExist:
                    raise serializers.ValidationError(_('No active account found with the given credentials.'))

            # If user is found with email or username, set username in attributes
            attrs['username'] = user.username


        # Continue with the normal validation process
        data = super().validate(attrs)
        user = self.user
        logged_user = User.objects.get(email=username_or_email) if '@' in username_or_email else User.objects.get(username=username_or_email)

        # Check if the user has any groups and assign a default role if not
        if not user.groups.exists():
            try:
                assign_role(user, 'nao_autenticado')  # Assigns a default role to the user
                print('User successfully added to the group.')
            except Exception as e:
                print(f'Error adding user to the group: {e}')
        
        # If the user is authenticated, record their login details
        if user.is_authenticated: 
            public_user_ip = self.get_public_ip()
            user_location = self.get_location(public_user_ip)

            user_agent_info = self.get_user_agent_info(request)
            print(user_agent_info)


            brasilia_tz = pytz.timezone('America/Sao_Paulo')
            current_date = timezone.now().astimezone(brasilia_tz)
            print("Adjusted date and time for Brasília:", current_date)
            try:
                # Save the login details in the DashboardData model
                register = dashModels.DashboardData(
                    user=logged_user,
                    last_date_login=current_date,
                    location=user_location,
                    ip=public_user_ip,
                    browser=user_agent_info['browser'],
                    type_device=user_agent_info['device'] 
                )
                register.save()
                print(f"Access recorded successfully: {register}")
            except Exception as e:
                print(f"Error recording user access: {e}")

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Customizes the token obtain pair view to use the custom serializer.

    Attributes:
    - serializer_class: Specifies the custom serializer to be used for token generation.
    """
    serializer_class = CustomTokenObtainPairSerializer

class ChangePassword(views.APIView):
    """ChangePassword APIView."""

    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        """Method to receive POST data from request.

        Args:
            oldPassword (str): old password
            newPassword (str): new password

        Returns:
            response: response data
        """

        old_password = request.data['oldPassword']
        new_password1 = request.data['newPassword1']

        if request.user.check_password(old_password):
            request.user.set_password(new_password1)
            request.user.save()

            refresh = RefreshToken.for_user(request.user)

            return response.Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            message = _('Incorrect password.')

        return response.Response(
            {'message': message}, status=status.HTTP_400_BAD_REQUEST
        )

class ResetPassword(views.APIView):
    serializer_class = usrSerializers.PasswordResetRequestSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        if email.endswith('@funai.gov.br'):
            return response.Response({
                "detail": "Usuários FUNAI não podem alterar o e-mail através do CMR. Para recuperar sua senha, por favor, entre em contato com o setor de TI da sua instituição."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return response.Response({"detail": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        usrModels.PasswordResetCode.objects.filter(user=user).delete()

        # Generate reset code
        reset_code = usrModels.PasswordResetCode.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(minutes=15)  # Expires in 15 minutes
        )

        reset_link = f"http://localhost:3000/password-reset/confirm/?code={reset_code.code}"

        subject = 'Solicitação de Recuperação de Senha do CMR'
        message = f'Foi solicitado a alteração de senha para o usuário {email}. Use o seguinte link para redefinir sua senha: {reset_link}'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Send email with the reset code
        try:
            send_mail(subject, message, from_email, [email], fail_silently=False)
            return response.Response({"detail": "Password reset code sent."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = usrSerializers.PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = self.request.query_params.get('code')
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']
        
        if new_password != confirm_password:
            return response.Response({"detail": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            reset_code = usrModels.PasswordResetCode.objects.get(code=code)
        except usrModels.PasswordResetCode.DoesNotExist:
            return response.Response({"detail": "Invalid or expired reset code."}, status=status.HTTP_400_BAD_REQUEST)
        
        if reset_code.is_expired():
            return response.Response({"detail": "Reset code has expired."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = reset_code.user
        user.set_password(new_password)
        user.save()
        
        # Delete the reset code
        reset_code.delete()
        
        return response.Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)