from rest_framework import (
    views,
    response
)
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import views, status
from authorization import utils

from authorization import constant

from rolepermissions.roles import assign_role, registered_roles, clear_roles
from rolepermissions.permissions import grant_permission, revoke_permission, get_user_roles
from rolepermissions.exceptions import RolePermissionScopeException

from django.conf import settings

class RequestPermissions(views.APIView):
    """
        API view to check and return the permissions of the logged-in user and a specific role.
    """
    def get(self, request):
        """
            Handles GET requests to retrieve user permissions and role permissions.

            Args:
            - request: The request object.

            Returns:
            - Response: JSON response containing user permissions.
        """
        current_user = request.user

        # Collect basic user information
        user_data = {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
        }

        # Check permissions for a specific role
        role_name = 'funai_cmr_admin'
        role = registered_roles.get(role_name)
        if role:
            print(f"ROLE_PERMISSIONS for {role_name}: {role.available_permissions}")
        else:
            print(f"Role '{role_name}' not found")

        # Check permissions of the logged-in user
        user_roles = get_user_roles(current_user)
        user_permissions = []
        for role in user_roles:
            # Get the available permissions for the current role
            role_permissions = role.available_permissions
            # Add the role permissions to the user's permission list
            user_permissions.extend(role_permissions.keys())
            print(f"USER_PERMISSIONS: {user_permissions}")
        return response.Response({'user_permissions': user_permissions})   

class GrantPermissions(views.APIView):
    """
        API view to grant specific permissions and roles to a user.
    """
   
    def clear_all(self, user):
        """
            Clears all permissions for the user.

            Args:
            - user: The user object.

            Returns:
            - list: List of user roles after clearing.
        """
        user_roles = get_user_roles(user)
        user_permissions = []
        for role in user_roles:
            # Get the available permissions for the current role
            role_permissions = role.available_permissions
            # Add the role permissions to the user's permission list
            user_permissions.extend(role_permissions.keys())
            for perm_name in role_permissions:
                revoke_permission(user, perm_name)   
        return user_roles
    
    def post(self, request):
        """
            Handles POST requests to grant permissions and roles to a user.

            Args:
            - request: The request object containing email, permissions, and role data.

            Returns:
            - Response: JSON response confirming permissions granted.
        """
        email = request.data.get('email')
        permissions = request.data.get('permissions', [])
        role = request.data.get('role')
        User = get_user_model()
        is_staff = request.data.get('is_staff', False)  # Optional, defaults to False
        is_superuser = request.data.get('is_superuser', False)  # Optional, defaults to False

        try:
            user = User.objects.get(email=email)
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            print(user_data)
        except User.DoesNotExist:
            return response.Response({'detail': f'Usuário com email {email} não encontrado.'}, status=404)
        
        # Check if the provided role exists
        if role not in registered_roles:
            return response.Response({'detail': f'A role {role} não existe.'}, status=400)
        
        role_class = registered_roles[role]
        role_permissions = role_class.available_permissions

        # Clear all existing roles and assign the specific role
        clear_roles(user)
        assign_role(user, role)

        self.clear_all(user)

        # List granted permissions to the user
        granted_permissions = []
        for perm_name, is_granted in role_permissions.items():
            if is_granted:
                grant_permission(user, perm_name)
                granted_permissions.append(perm_name)
        
         # Update user's staff and superuser status
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        # Send email to the user
        subject = 'Alteração nas suas permissões de acesso do CMR'
        message = f'Prezado(a) {user.username}, suas permissões de acesso do CMR foram alteradas. Por favor, acesse https://cmr.funai.gov.br/ para verificá-las.'
        from_email = 'hexgisdev@gmail.com'
        recipient_list = [email, 'valdean.junior@hex360.com.br']
        
        # try:
        #     utils.send_custom_email(subject, message, from_email, recipient_list, request.user)
        #     print("E-mail enviado com sucesso!")
        # except Exception as e:
        #     return response.Response({'detail': f'Erro ao enviar o e-mail: {str(e)}'}, status=500)

        # Retornar detalhes das permissões concedidas
        return response.Response({
            'detail': f'Permissões concedidas para o usuário com email {email}.',
            'role': role,
            'permissions': granted_permissions,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        }, status=200)

class RevokePermissions(views.APIView):
    """
        API view to revoke specific permissions from a user.
    """
    
    def post(self, request):
        """
            Handles POST requests to revoke permissions from a user.

            Args:
            - request: The request object containing email and permissions data.

            Returns:
            - Response: JSON response confirming permission revocation.
        """
        email = request.data.get('email')
        permissions = request.data.get('permissions', [])
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            print(user_data)
        except User.DoesNotExist:
            return response.Response({'detail': f'Usuário com email {email} não encontrado.'}, status=404)
        
        try:
            # Revoke each permission provided in the request
            for permission in permissions:
                revoke_permission(user, permission)
        except RolePermissionScopeException:
            return response.Response({'detail': 'Este usuário não possui as permissões informadas.'}, status=400)

        return response.Response({'detail': f'Permissão revogada para o usuário com email {email}.'})


class SendEmailTest(views.APIView):
    """
        API view to send a test email.
    """
    
    def post(self, request):
        """
            Handles POST requests to send a test email.

            Args:
            - request: The request object containing subject and message data.

            Returns:
            - JsonResponse: JSON response confirming if the email was sent successfully or providing an error message.
        """
        subject = request.data.get('subject')
        message = request.data.get('message')
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['valdean.junior@hex360.com.br']  # Example recipient list

        try:
            # Call the send_custom_email function from your utils module
            utils.send_custom_email(subject, message, from_email, recipient_list, request.user)
            return JsonResponse({'message': 'Email enviado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LoggedUserPermissions(views.APIView):
    """Logged in user permissions."""

    def get(self, request, *args, **kwargs):
        """Lists all permissions associated to the logged in user."""
        return response.Response(request.user.get_all_permissions())


class LoggedUserCMRModules(views.APIView):
    """Logged in user access."""

    def get(self, request, *args, **kwargs):
        """Informs which 'CMR2 Modules' the logged in user has access to."""
        perms_cmrmodules = dict()

        for cmrmodules in list(constant.CMR_MODULES.keys()):
            perms_cmrmodules.update({cmrmodules: request.user.has_perms(constant.CMR_MODULES[cmrmodules]["access"])})

        return response.Response(perms_cmrmodules)

