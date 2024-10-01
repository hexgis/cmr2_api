from django.contrib.gis import admin

from catalog import models

from cmr2_api.mixins import AdminPermissionMixin
from rolepermissions.permissions import get_user_roles, available_perm_status


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

class SatelliteAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """
        Django Administrator for `model.Satellite` data.
        Manages permissions for viewing, changing, and adding satellite data.
    """
    
    def has_view_permission(self, request, obj=None):
        """
            Determines if the user has permission to view satellite data.

            Args:
            - request: The HTTP request object.
            - obj: The object being accessed (default is None).

            Returns:
            - bool: True if the user has 'visualizar_catalog' permission, False otherwise.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_catalog' and perm_status:
                    return True
            
            return super().has_view_permission(request, obj)
        except Exception as e:
            # Adicione logging aqui se desejar
            print(f"Erro ao verificar permissão de visualização: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
            Determines if the user has permission to change satellite data.

            Args:
            - request: The HTTP request object.
            - obj: The object being accessed (default is None).

            Returns:
            - bool: True if the user has 'alterar_catalog' permission, False otherwise.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_catalog' and perm_status:
                    return True

            return super().has_change_permission(request, obj)
        except Exception as e:
            # Adicione logging aqui se desejar
            print(f"Erro ao verificar permissão de alteração: {e}")
            return False  
    
    def has_add_permission(self, request):
        """
            Determines if the user has permission to change satellite data.

            Args:
            - request: The HTTP request object.
            - obj: The object being accessed (default is None).

            Returns:
            - bool: True if the user has 'alterar_catalog' permission, False otherwise.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_catalog' and perm_status:
                    return True

            return super().has_add_permission(request)
        except Exception as e:
            # Adicione logging aqui se desejar
            print(f"Erro ao verificar permissão de adição: {e}")
            return False        
        
    list_display = (
        'identifier',
        'name',
        'description',
    )

    fields = list_display

    search_fields = list_display


class SceneAdmin(AdminPermissionMixin, admin.GeoModelAdmin):
    """
        Django Administrator for `model.Scene` data.
        Manages permissions for viewing, changing, and adding Secene admin.
    """
    def has_view_permission(self, request, obj=None):
        """
            Determines if the user has permission to view satellite data.

            Args:
            - request: The HTTP request object.
            - obj: The object being accessed (default is None).

            Returns:
            - bool: True if the user has 'visualizar_catalog' permission, False otherwise.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_catalog' and perm_status:
                    return True
            
            return super().has_view_permission(request, obj)
        except Exception as e:
            # Adicione logging aqui se desejar
            print(f"Erro ao verificar permissão de visualização: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
            Determines if the user has permission to change satellite data.

            Args:
            - request: The HTTP request object.
            - obj: The object being accessed (default is None).

            Returns:
            - bool: True if the user has 'alterar_catalog' permission, False otherwise.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_catalog' and perm_status:
                    return True

            return super().has_change_permission(request, obj)
        except Exception as e:
            # Adicione logging aqui se desejar
            print(f"Erro ao verificar permissão de alteração: {e}")
            return False  
    
    def has_add_permission(self, request):
        """
            Determines if the user has permission to change satellite data.

            Args:
            - request: The HTTP request object.
            - obj: The object being accessed (default is None).

            Returns:
            - bool: True if the user has 'alterar_catalog' permission, False otherwise.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_catalog' and perm_status:
                    return True

            return super().has_add_permission(request)
        except Exception as e:
            # Adicione logging aqui se desejar
            print(f"Erro ao verificar permissão de adição: {e}")
            return False    
        
    def cloud_cover_percent(self, instance:models.Scene)-> str:
        """_summary_

        Args:
            instance (models.Scene): Scene models data

        Returns:
            str: cloud cover in percent.
        """

        return '{}%'.format(instance.cloud_cover)
    
    # Displayed fields in the list view
    list_display = (
        'image',
        'type',
        'date',
        'pr_date',
        'locator',
        'sat_identifier',
        'sat_name',
    )

    # Fields displayed in the form view
    fields = (
        'image',
        'type',
        'image_path',
        'url_tms',
        'preview',
        'date',
        'cloud_cover_percent',
        'locator',
        'geom',
        'sat_identifier',
        'sat_name',
    )

    # Fields used for searching in the admin interface
    search_fields = ('image',)

    list_filter = ('date', )

    readonly_fields = fields


admin.site.register(models.Scene, SceneAdmin)
admin.site.register(models.Satellite, SatelliteAdmin)
