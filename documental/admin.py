from django.contrib import admin

from documental import models
from cmr2_api.mixins import AdminPermissionMixin
from rolepermissions.permissions import get_user_roles, available_perm_status


"""List of common fields for DjangoAdmin classes."""
list_fields_admin_commun = [
    'file',
    'id_document',
    'path_document',
    'no_document',
    'usercmr_id',
    'st_available',
    'st_excluded',
    'co_funai',
    'no_ti',
    'co_cr',
    'ds_cr',
    'action_id',
]

def get_user_permissions(user):
    """
        Retrieves the permissions of a given user based on their roles.

        Args:
        - user: The user object for whom permissions are to be retrieved.

        Returns:
        - tuple: A tuple containing two elements:
            - permissions_list: List of tuples where each tuple contains a permission name and its status (True/False).
            - user_role: List of roles assigned to the user.
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

class DocsActionAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Django administrator for `models.DocsAction` data."""

    def has_view_permission(self, request, obj=None):
        """
        Checks if the user has permission to view the `DocsAction` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_documental_acoes' and perm_status:
                    return True
            return super().has_view_permission(request, obj)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
        Checks if the user has permission to change the `DocsAction` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_documental_acoes' and perm_status:
                    return True
            return super().has_change_permission(request, obj)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking change permission: {e}")
            return False       

    def has_add_permission(self, request):
        """
        Checks if the user has permission to add to the `DocsAction` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_documental_acoes' and perm_status:
                    return True
            return super().has_add_permission(request)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking add permission: {e}")
            return False    

    list_display = (
        'id_action',
        'no_action',
        'dt_creation',
        'action_type',
        'action_type_group',
        'description',
    )

    fields = list_display

    search_fields = list_display

class UsersCMRAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Django administrator for `model.Usuario` data."""

    def has_view_permission(self, request, obj=None):
        """
        Checks if the user has permission to view the `Usuarios` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_documental_usuarios_cmr' and perm_status:
                    return True
            return super().has_view_permission(request, obj)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
        Checks if the user has permission to change the `Usuarios` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_documental_usuarios_cmr' and perm_status:
                    return True
            return super().has_change_permission(request, obj)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking change permission: {e}")
            return False       

    def has_add_permission(self, request):
        """
        Checks if the user has permission to add to the `Usuarios` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_documental_usuarios_cmr' and perm_status:
                    return True
            return super().has_add_permission(request)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking add permission: {e}")
            return False


    list_display = (
        'id_user',
        'first_name',
    )

    fields = list_display

    search_fields = list_display

class DocsDocumentTIAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Django administrator for `model.DocsDocumentTI` data."""

    def has_view_permission(self, request, obj=None):
        """
        Checks if the user has permission to view the `DocsDocumentTI` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_documental_terras_indigenas' and perm_status:
                    return True
            
            return super().has_view_permission(request, obj)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
        Checks if the user has permission to change the `DocsDocumentTI` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_documental_terras_indigenas' and perm_status:
                    return True
            return super().has_change_permission(request, obj)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking change permission: {e}")
            return False       

    def has_add_permission(self, request):
        """
        Checks if the user has permission to add to the `DocsDocumentTI` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_documental_usuarios_cmr' and perm_status:
                    return True
            return super().has_add_permission(request)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking add permission: {e}")
            return False

    list_display = [
        'no_extension',
        'dt_document',
        'dt_registration',
    ] + list_fields_admin_commun

    fields = list_fields_admin_commun

    search_fields = list_fields_admin_commun

class DocsLandUserAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Django administrator for `model.DocsLandUser` data."""

    def has_view_permission(self, request, obj=None):
        """
        Checks if the user has permission to view the `DocsLandUser` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_documental_terras_usuario' and perm_status:
                    return True
            
            return super().has_view_permission(request, obj)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
        Checks if the user has permission to change the `DocsLandUser` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_documental_terras_usuario' and perm_status:
                    return True
            return super().has_change_permission(request, obj)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking change permission: {e}")
            return False       

    def has_add_permission(self, request):
        """
        Checks if the user has permission to add to the `DocsLandUser` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_documental_terras_usuario' and perm_status:
                    return True
            return super().has_add_permission(request)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking add permission: {e}")
            return False

    list_display = [
        'nu_year',
        'nu_year_map',
        'dt_registration',
    ] + list_fields_admin_commun

    fields = list_fields_admin_commun

    search_fields = list_fields_admin_commun

class DocsMapotecaAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Django administrator for `model.DocsMapoteca` data."""

    def has_view_permission(self, request, obj=None):
        """
        Checks if the user has permission to view the `DocsMapoteca` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_documental_mapoteca' and perm_status:
                    return True
            
            return super().has_view_permission(request, obj)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
        Checks if the user has permission to change the `DocsMapoteca` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_documental_mapoteca' and perm_status:
                    return True
            return super().has_change_permission(request, obj)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking change permission: {e}")
            return False       

    def has_add_permission(self, request):
        """
        Checks if the user has permission to add to the `DocsMapoteca` model.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_documental_mapoteca' and perm_status:
                    return True
            return super().has_add_permission(request)
        except Exception as e:
            # Add logging here if desired
            print(f"Error checking add permission: {e}")
            return False

    list_display = [
        'no_description',
        'map_dimension',
        'js_ti',
        'dt_registration',
    ] + list_fields_admin_commun

    fields = list_fields_admin_commun

    search_fields = list_fields_admin_commun

admin.site.register(models.DocsAction, DocsActionAdmin)
admin.site.register(models.UsersCMR, UsersCMRAdmin)
admin.site.register(models.DocsDocumentTI, DocsDocumentTIAdmin)
admin.site.register(models.DocsLandUser, DocsLandUserAdmin)
admin.site.register(models.DocsMapoteca, DocsMapotecaAdmin)
