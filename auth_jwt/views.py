from django.utils.translation import ugettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rolepermissions.roles import assign_role
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


from rest_framework import (
    response,
    permissions,
    views,
    status
)

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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
        Customizes the token obtain pair serializer to add additional functionalities.
    """
    username_field = 'username'
    email = serializers.EmailField(required=False)

    def validate(self, attrs):
        """
            Validates the token obtain pair request and performs additional actions.

            Args:
            - attrs (dict): Dictionary of request attributes.

            Returns:
            - dict: Validated data dictionary.
        """
        data = super().validate(attrs)
        user = self.user
        if not user.groups.exists():
            try:
                assign_role(user, 'nao_autenticado') # Assigns a role to the user if not already assigned
                print('Usuário adicionado ao grupo com sucesso')
            except Exception as e:
                print(f'Erro ao adicionar usuário ao grupo: {e}')
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    """
        Customizes the token obtain pair view to use the custom serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer