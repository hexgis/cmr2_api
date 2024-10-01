from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny

from user_agents import parse as parse_user_agent

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail

import requests 
import pytz
import uuid

from rest_framework import (
    response,
    permissions,
    views,
    status,
    serializers,
    generics
)

from datetime import timedelta

from user_profile import models as usrModels
from user_profile import serializers as usrSerializers
from dashboard import models as dashModels

User = get_user_model()

import logging

logger = logging.getLogger(__name__)


from django.template.loader import render_to_string

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
                return {
                    'city': data.get('city'),
                    'region': data.get('region'),
                    'country_name': data.get('country_name'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude')
                }
            else:
                return {'error': 'Unknown location'}
        except Exception as e:
            return {'error': f'Error fetching location: {e}'}
    
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
        
        # If the user is authenticated, record their login details
        if user.is_authenticated: 
            public_user_ip = self.get_public_ip()
            user_location = self.get_location(public_user_ip)

            user_agent_info = self.get_user_agent_info(request)
            latitudeF = user_location.get('latitude')
            longitudeF = user_location.get('longitude')

            brasilia_tz = pytz.timezone('America/Sao_Paulo')
            current_date = timezone.now().astimezone(brasilia_tz)

            try:
                # Save the login details in the DashboardData model
                register = dashModels.DashboardData(
                    user=logged_user,
                    last_date_login=current_date,
                    location=f"{user_location.get('city')}, {user_location.get('region')}, {user_location.get('country_name')}",
                    ip=public_user_ip,
                    browser=user_agent_info['browser'],
                    type_device=user_agent_info['device'],
                    latitude=latitudeF,
                    longitude=longitudeF,
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

class ResetPassword(views.APIView):
    """Endpoint to handle password reset requests."""

    serializer_class = usrSerializers.PasswordResetRequestSerializer
    permission_classes = [AllowAny]
    authentication_classes = [] 
    
    def post(self, request, *args, **kwargs):
        """Handles POST requests to reset a user's password."""
        # Validate request data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Restrict password reset for FUNAI email addresses
        if email.endswith('@funai.gov.br'):
            return response.Response({
                "detail": "Usuários FUNAI não podem alterar o e-mail através do CMR. "
                          "Para recuperar sua senha, por favor, entre em contato com o setor de TI da sua instituição."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user with provided email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return response.Response({"detail": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete any existing reset codes for this user
        usrModels.PasswordResetCode.objects.filter(user=user).delete()

        # Generate a new reset code with a 15-minute expiration
        reset_code = usrModels.PasswordResetCode.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(minutes=15)
        )
            
        # Generate password reset link
        reset_link = settings.RESET_PASSWORD_URL.format(code=reset_code.code)

        # Prepare email content with reset link and code
        context = {
            'user': user,
            'reset_link': reset_link,
            'reset_code': reset_code.code
        }
        html_message = render_to_string('email/password_reset.html', context)

        subject = 'Solicitação de Recuperação de Senha do CMR'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Send the password reset email
        try:
            send_mail(subject, message='', from_email=from_email, recipient_list=[email], html_message=html_message)
            return response.Response({"detail": "Password reset code sent."}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle email sending errors
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetConfirmView(generics.GenericAPIView):
    """Endpoint to confirm and process a password reset."""
    serializer_class = usrSerializers.PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        """Handles POST requests to reset the user's password."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Checks that the 'code' parameter has been supplied
        code =  request.data.get('code')
        if not code:
            return response.Response({"detail": "Reset code is required."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        if new_password != confirm_password:
            return response.Response({"detail": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset_code = usrModels.PasswordResetCode.objects.get(code=code)
        except usrModels.PasswordResetCode.DoesNotExist:
            return response.Response({"detail": "Invalid or expired reset code."}, status=status.HTTP_400_BAD_REQUEST)

        if reset_code.is_expired():
            return response.Response({"detail": "Reset code has expired."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        user = reset_code.user
        user.set_password(new_password)
        user.save()

        reset_code.delete()

        return response.Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)



