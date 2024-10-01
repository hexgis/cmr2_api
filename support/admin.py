from django.contrib import admin

from support import models
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

class GeoserverAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Admin interface for managing Geoserver instances."""

    def has_view_permission(self, request, obj=None):
        try:
            # Check if the user has specific permission to view Geoserver instances
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_support' and perm_status:
                    return True
            
            # If no specific permission found, fallback to default permission check
            return super().has_view_permission(request, obj)
        except Exception as e:
            # Handle any exceptions that occur during permission check
            # Optionally, add logging here for debugging purposes
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        try:
            # Check if the user has specific permission to change Geoserver instances
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_support' and perm_status:
                    return True

            # If no specific permission found, fallback to default permission check
            return super().has_change_permission(request, obj)
        except Exception as e:
            # Handle any exceptions that occur during permission check
            # Optionally, add logging here for debugging purposes
            print(f"Error checking change permission: {e}")
            return False  
    
    def has_add_permission(self, request):
        try:
            # Check if the user has specific permission to add new Geoserver instances
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_support' and perm_status:
                    return True

            # If no specific permission found, fallback to default permission check
            return super().has_add_permission(request)
        except Exception as e:
            # Handle any exceptions that occur during permission check
            # Optionally, add logging here for debugging purposes
            print(f"Error checking add permission: {e}")
            return False    

    list_display = (
        'name',
        'wms_url',
        'preview_url',
    )
    fields = list_display  # Display fields in the admin interface
    search_fields = list_display  # Enable searching by these fields in admin interface

class CategoryLayersGroupAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Admin interface for managing CategoryLayersGroup instances."""

    def has_view_permission(self, request, obj=None):
        try:
            # Check if the user has specific permission to view CategoryLayersGroup instances
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_support' and perm_status:
                    return True
            
            # If no specific permission found, fallback to default permission check
            return super().has_view_permission(request, obj)
        except Exception as e:
            # Handle any exceptions that occur during permission check
            # Optionally, add logging here for debugging purposes
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        try:
            # Check if the user has specific permission to change CategoryLayersGroup instances
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_support' and perm_status:
                    return True

            # If no specific permission found, fallback to default permission check
            return super().has_change_permission(request, obj)
        except Exception as e:
            # Handle any exceptions that occur during permission check
            # Optionally, add logging here for debugging purposes
            print(f"Error checking change permission: {e}")
            return False  
    
    def has_add_permission(self, request):
        try:
            # Check if the user has specific permission to add new CategoryLayersGroup instances
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_support' and perm_status:
                    return True

            # If no specific permission found, fallback to default permission check
            return super().has_add_permission(request)
        except Exception as e:
            # Handle any exceptions that occur during permission check
            # Optionally, add logging here for debugging purposes
            print(f"Error checking add permission: {e}")
            return False    

    list_display = (
        'name',
        'icon',
        'description'
    )
    fields = ('name', 'icon', 'description')  # Specify fields to display/edit in the admin interface
    search_fields = ('name', 'description')   # Enable searching by these fields in admin interface

class LayersGroupAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Admin interface for managing LayersGroup instances."""

    def has_view_permission(self, request, obj=None):
        try:
            # Check if the user has specific permission to view LayersGroup instances
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_support' and perm_status:
                    return True
            
            # If no specific permission found, fallback to default permission check
            return super().has_view_permission(request, obj)
        except Exception as e:
            # Handle any exceptions that occur during permission check
            # Optionally, add logging here for debugging purposes
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        try:
            # Check if the user has specific permission to change LayersGroup instances
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_support' and perm_status:
                    return True

            # If no specific permission found, fallback to default permission check
            return super().has_change_permission(request, obj)
        except Exception as e:
            # Handle any exceptions that occur during permission check
            # Optionally, add logging here for debugging purposes
            print(f"Error checking change permission: {e}")
            return False  
    
    def has_add_permission(self, request):
        try:
            # Check if the user has specific permission to add new LayersGroup instances
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_support' and perm_status:
                    return True

            # If no specific permission found, fallback to default permission check
            return super().has_add_permission(request)
        except Exception as e:
            # Handle any exceptions that occur during permission check
            # Optionally, add logging here for debugging purposes
            print(f"Error checking add permission: {e}")
            return False

    list_display = (
        'name',
        'order',
        'category_groups'
    )
    fields = ('name', 'order', 'category_groups')  # Specify fields to display/edit in the admin interface
    search_fields = ('name', 'category_groups__name')  # Enable searching by these fields in admin interface

class LayerAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Admin interface for managing LayerAdmin instances."""

    def has_view_permission(self, request, obj=None):
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_support' and perm_status:
                    return True
            
            return super().has_view_permission(request, obj)
        except Exception as e:
            # Optionally add logging here for debugging
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_support' and perm_status:
                    return True

            return super().has_change_permission(request, obj)
        except Exception as e:
            # Optionally add logging here for debugging
            print(f"Error checking change permission: {e}")
            return False  
    
    def has_add_permission(self, request):
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_support' and perm_status:
                    return True

            return super().has_add_permission(request)
        except Exception as e:
            # Optionally add logging here for debugging
            print(f"Error checking add permission: {e}")
            return False
        
    list_display = (
        'name',
        'order',
        'layer_type',
        'active_on_init',
        'layers_group',
        'is_public',
    )

    fields = ('name', 'order', 'layer_type', 'active_on_init', 'layers_group', 'is_public')
    
    search_fields = (
        'name',
        'layers_group__name',
    )

    list_filter = (
        'layer_type',
        'is_public',
    )



class WmsLayerAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """
    Admin configuration for managing WMS Layers with permission checks.

    Permissions:
    - 'visualizar_support': Allows viewing WMS layers.
    - 'alterar_support': Allows changing WMS layers.
    - 'adicionar_support': Allows adding new WMS layers.
    """

    def has_view_permission(self, request, obj=None):
        """
        Check if the current user has permission to view WMS layers.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_support' and perm_status:
                    return True
            
            # Fall back to default permission check if specific permission not found
            return super().has_view_permission(request, obj)
        
        except Exception as e:
            # Log any errors that occur during permission check
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
        Check if the current user has permission to change WMS layers.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_support' and perm_status:
                    return True

            # Fall back to default permission check if specific permission not found
            return super().has_change_permission(request, obj)
        
        except Exception as e:
            # Log any errors that occur during permission check
            print(f"Error checking change permission: {e}")
            return False  
    
    def has_add_permission(self, request):
        """
        Check if the current user has permission to add new WMS layers.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_support' and perm_status:
                    return True

            # Fall back to default permission check if specific permission not found
            return super().has_add_permission(request)
        
        except Exception as e:
            # Log any errors that occur during permission check
            print(f"Error checking add permission: {e}")
            return False
        
    list_display = (
        'layer',
        'geoserver_layer_name',
        'geoserver_layer_namespace',
        'geoserver',
        'has_preview',
        'has_detail',
        'detail_width',
    )

    fields = (
        'layer',
        'geoserver_layer_name',
        'geoserver_layer_namespace',
        'geoserver',
        'geoserver_layer_options',
        'has_preview',
        'has_detail',
        'detail_width',
        'has_opacity',
        'queryable',
        'default_opacity',
    )
    
    search_fields = (
        'geoserver_layer_name',
        'geoserver_layer_namespace',
    )

    list_filter = (
        'geoserver',
        'has_preview',
        'has_detail',
        'geoserver_layer_namespace',
    )

    list_per_page = 25

class TmsLayerAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """
    Admin configuration for managing TMS Layers with permission checks.

    Permissions:
    - 'visualizar_support': Allows viewing TMS layers.
    - 'alterar_support': Allows changing TMS layers.
    - 'adicionar_support': Allows adding new TMS layers.
    """

    def has_view_permission(self, request, obj=None):
        """
        Check if the current user has permission to view TMS layers.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_support' and perm_status:
                    return True
            
            # Fall back to default permission check if specific permission not found
            return super().has_view_permission(request, obj)
        
        except Exception as e:
            # Log any errors that occur during permission check
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
        Check if the current user has permission to change TMS layers.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_support' and perm_status:
                    return True

            # Fall back to default permission check if specific permission not found
            return super().has_change_permission(request, obj)
        
        except Exception as e:
            # Log any errors that occur during permission check
            print(f"Error checking change permission: {e}")
            return False  
    
    def has_add_permission(self, request):
        """
        Check if the current user has permission to add new TMS layers.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_support' and perm_status:
                    return True

            # Fall back to default permission check if specific permission not found
            return super().has_add_permission(request)
        
        except Exception as e:
            # Log any errors that occur during permission check
            print(f"Error checking add permission: {e}")
            return False
        
    list_display = (
        'layer',
        'url_tms',
        'date',
        'max_native_zoom',
    )

    fields = list_display

    search_fields = (
        'date',
    )

    list_filter = (
        'max_native_zoom',
    )

class LayerFilterAdmin(AdminPermissionMixin,admin.ModelAdmin):
    """
    Admin configuration for managing Layer Filters with permission checks.

    Permissions:
    - 'visualizar_support': Allows viewing Layer Filters.
    - 'alterar_support': Allows changing Layer Filters.
    - 'adicionar_support': Allows adding new Layer Filters.
    """

    def has_view_permission(self, request, obj=None):
        """
        Check if the current user has permission to view Layer Filters.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_support' and perm_status:
                    return True
            # Fall back to default permission check if specific permission not found
            return super().has_view_permission(request, obj)
        except Exception as e:
            # Log any errors that occur during permission check
            print(f"Erro ao verificar permissão de visualização: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
        Check if the current user has permission to change Layer Filters.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_support' and perm_status:
                    return True
            # Fall back to default permission check if specific permission not found
            return super().has_change_permission(request, obj)
        except Exception as e:
            # Log any errors that occur during permission check
            print(f"Erro ao verificar permissão de alteração: {e}")
            return False  
    
    def has_add_permission(self, request):
        """
        Check if the current user has permission to add new Layer Filters.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_support' and perm_status:
                    return True

            # Fall back to default permission check if specific permission not found
            return super().has_add_permission(request)
        
        except Exception as e:
            # Log any errors that occur during permission check
            print(f"Error checking add permission: {e}")
            return False
        
    list_display = (
        'label',
        'default',
        'filter_type',
        'filter_alias',
    )

    fields = (
        'default',
        'filter_type',
        'label',
        'layers',
        'filter_alias',
    )

    list_filter = (
        'filter_alias',
        'filter_type',
    )


admin.site.register(models.Geoserver, GeoserverAdmin)
admin.site.register(models.LayersGroup, LayersGroupAdmin)
admin.site.register(models.Layer, LayerAdmin)
admin.site.register(models.WmsLayer, WmsLayerAdmin)
admin.site.register(models.TmsLayer, TmsLayerAdmin)
admin.site.register(models.CategoryLayersGroup, CategoryLayersGroupAdmin)
admin.site.register(models.LayerFilter, LayerFilterAdmin)
