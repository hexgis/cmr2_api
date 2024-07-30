from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from cmr2_api.mixins import AdminPermissionMixin
from rolepermissions.permissions import get_user_roles, available_perm_status
from rolepermissions.roles import registered_roles

from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserChangeForm

# Deregister standard templates
admin.site.unregister(Group)
admin.site.unregister(User)

# Re-register Group template with permission checks applied
@admin.register(Group)
class CustomGroupAdmin(AdminPermissionMixin, GroupAdmin):
    """ 
        Customizes the group admin panel with permission-based views and actions.
    """
    def user_permissions(self, user):
        """
            Retrieves the effective permissions for the given user.

            Args:
            - user (User): The user object.

            Returns:
            - list: List of tuples containing permission names and their status.
            - list: List of user roles.
        """
        user_permissions = []
        permissions_list = []
        user_role = get_user_roles(user)
        for role in user_role:
            role_permissions = role.available_permissions
            user_permissions.extend(role_permissions.keys())

        for perm_name in user_permissions:
            permissions = available_perm_status(user)
            permissions_list.append((perm_name, permissions.get(perm_name, False)))

        return permissions_list, user_role 

    def has_view_permission(self, request, obj=None):
        """
        Checks if the current user has permission to view the group admin panel.

        Args:
        - request: The request object.
        - obj: Optional object instance.

        Returns:
        - bool: True if the user has permission; False otherwise.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = self.user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_painel_grupos' and perm_status:
                    return True
            
            return super().has_view_permission(request, obj)
        except Exception as e:
            
            print(f"Erro ao verificar permissão de visualização: {e}")
            return False

    def has_change_permission(self, request, obj=None):
        """
            Checks if the current user has permission to change group.

            Args:
            - request: The request object.
            - obj: Optional object instance.

            Returns:
            - bool: True if the user has permission; False otherwise.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = self.user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_grupo' and perm_status:
                    return True

            return super().has_change_permission(request, obj)
        except Exception as e:
            
            print(f"Erro ao verificar permissão de alteração: {e}")
            return False            

    def has_add_permission(self, request):
        """
            Checks if the current user has permission to add new groups.

            Args:
            - request: The request object.

            Returns:
            - bool: True if the user has permission; False otherwise.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = self.user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_grupo' and perm_status:
                    return True

            return super().has_add_permission(request)
        except Exception as e:
            
            print(f"Erro ao verificar permissão de alteração: {e}")
            return False
def get_permissions_for_role(role_name):
    """
        Retrieves permissions available for a given role.

        Args:
        - role_name (str): The name of the role.

        Returns:
        - dict: Dictionary of permissions available for the role.
    """
    role = registered_roles.get(role_name)
    if role:
        return {perm: val for perm, val in role.available_permissions.items() if val}
    return {}

class CustomUserChangeForm(UserChangeForm):
    """ 
        Customizes the user change form based on user roles and permissions.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            user_roles = get_user_roles(self.instance)
            role_permissions = {}
            for role in user_roles:
                role_permissions.update(get_permissions_for_role(role.get_name()))

            codenames = role_permissions.keys()
            # Filters available permissions to show only those specific to user roles
            self.fields['user_permissions'].queryset = Permission.objects.filter(
                codename__in=codenames,
                content_type__app_label='auth',
                content_type__model='user'
            )
            # Exclude a particular group from the list
            if any(role.get_name() != 'dev_master_admin' for role in user_roles):
                self.fields['groups'].queryset = Group.objects.exclude(name='dev_master_admin')

            if any(role.get_name() == 'funai_cmr_admin' for role in user_roles):
                # Enable fields for superuser role
                self.fields['is_active'].disabled = False
                self.fields['is_staff'].disabled = False
                self.fields['is_superuser'].disabled = False

                # Set initial values for superuser role
                self.initial['is_active'] = True
                self.initial['is_staff'] = True
                self.initial['is_superuser'] = True
            else:
                # Disable staff and superuser fields for non-superuser roles
                self.fields['is_active'].disabled = False
                self.fields['is_staff'].disabled = True
                self.fields['is_superuser'].disabled = True

# Re-register User template with permission checks applied
@admin.register(User)
class CustomUserAdmin(AdminPermissionMixin, UserAdmin):
    """ 
        Customizes the user admin panel with permission-based views and actions.
    """
    form = CustomUserChangeForm

    def user_permissions(self, user):
        """
            Retrieves the effective permissions for the given user.

            Args:
            - user (User): The user object.

            Returns:
            - list: List of tuples containing permission names and their status.
            - list: List of user roles.
        """
        user_permissions = []
        permissions_list = []
        user_role = get_user_roles(user)
        for role in user_role:
            role_permissions = role.available_permissions
            user_permissions.extend(role_permissions.keys())

        for perm_name in user_permissions:
            permissions = available_perm_status(user)
            permissions_list.append((perm_name, permissions.get(perm_name, False)))

        return permissions_list, user_role 

    def has_view_permission(self, request, obj=None):
        """
            Checks if the current user has permission to view user admin panel.

            Args:
            - request: The request object.
            - obj: Optional object instance.

            Returns:
            - bool: True if the user has permission; False otherwise.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = self.user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_painel_de_usuarios' and perm_status:
                    return True
            
            return super().has_view_permission(request, obj)
        except Exception as e:
            
            print(f"Erro ao verificar permissão de visualização: {e}")
            return False

    def has_change_permission(self, request, obj=None):
        """
            Checks if the current user has permission to change user details.

            Args:
            - request: The request object.
            - obj: Optional object instance.

            Returns:
            - bool: True if the user has permission; False otherwise.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = self.user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_usuario' and perm_status:
                    return True

            return super().has_change_permission(request, obj)
        except Exception as e:
            
            print(f"Erro ao verificar permissão de alteração: {e}")
            return False            

    def has_add_permission(self, request):
        """
            Checks if the current user has permission to add new users.

            Args:
            - request: The request object.

            Returns:
            - bool: True if the user has permission; False otherwise.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = self.user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_usuario' and perm_status:
                    return True

            return super().has_add_permission(request)
        except Exception as e:
            
            print(f"Erro ao verificar permissão de alteração: {e}")
            return False    
        

    def get_fieldsets(self, request, obj=None):
        """
            Defines the fieldsets to display based on user permissions.

            Args:
            - request: The request object.
            - obj: Optional object instance.

            Returns:
            - tuple: Fieldsets to display based on user permissions.
        """
        try:
            fieldsets = super().get_fieldsets(request, obj)
            user = request.user
            current_user_permissions, current_user_roles = self.user_permissions(user)
            
            if obj is None:  # Adicionando novo usuário
                return self.add_fieldsets

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_status_do_usuario' and perm_status:
                    return (
                        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
                        (None, {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                    )
                
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_grupo_do_usuario' and perm_status:
                    return (
                        (None, {'fields': ('groups', 'user_permissions')}),
                    )

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_permissoes_do_usuario' and perm_status:
                    return (
                        (None, {'fields': ('user_permissions',)}),
                    )

            return fieldsets
        except Exception as e:
            
            print(f"Erro ao obter fieldsets: {e}")
            return fieldsets

    def get_queryset(self, request):
        """
            Retrieves the queryset based on user permissions.

            Args:
            - request: The request object.

            Returns:
            - queryset: Filtered queryset based on user permissions.
        """
        try:
            qs = super().get_queryset(request)
            user = request.user
            current_user_permissions, current_user_roles = self.user_permissions(user)
            
            if any(role.get_name() == 'funai_cmr_admin' for role in current_user_roles):
                qs = qs.exclude(groups__name='dev_master_admin')
            
            return qs
        except Exception as e:
            
            print(f"Erro ao obter queryset: {e}")
            return super().get_queryset(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
            Customizes the change view for user admin.

            Args:
            - request: The request object.
            - object_id: ID of the object to change.
            - form_url: URL for the form.
            - extra_context: Additional context data.

            Returns:
            - HttpResponse: Response for the change view.
        """
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        """
            Customizes the add view for user admin.

            Args:
            - request: The request object.
            - form_url: URL for the form.
            - extra_context: Additional context data.

            Returns:
            - HttpResponse: Response for the add view.
        """
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save'] = False
        return super().add_view(request, form_url=form_url, extra_context=extra_context)