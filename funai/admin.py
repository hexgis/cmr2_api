from django.contrib import admin

from cmr2_api.mixins import AdminPermissionMixin

from funai import models
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

class CoordenacaoRegionalAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Admin model for CoordenacaoRegionalAdmin."""

    def has_view_permission(self, request, obj=None):
        """
        Checks if the user has permission to view CoordenacaoRegionalAdmin.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_funai_coordenacao_reginal' and perm_status:
                    return True
            
            return super().has_view_permission(request, obj)
        except Exception as e:
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
        Checks if the user has permission to change CoordenacaoRegionalAdmin.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_funai_coordenacao_reginal' and perm_status:
                    return True

            return super().has_change_permission(request, obj)
        except Exception as e:
            print(f"Error checking change permission: {e}")
            return False       

    def has_add_permission(self, request):
        """
        Checks if the user has permission to add to CoordenacaoRegionalAdmin.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_funai_coordenacao_reginal' and perm_status:
                    return True

            return super().has_add_permission(request)
        except Exception as e:
            print(f"Error checking add permission: {e}")
            return False    

    list_display = (
        'co_cr',
        'ds_cr',
        'no_abreviado',
        'sg_cr',
        'st_situacao',
        'ds_email',
        'no_regiao',
        'no_municipio',
        'no_uf',
        'sg_uf',
        'ds_telefone',
        'dt_cadastro',
    )

    search_fields = (
        'co_cr',
        'ds_cr',
        'no_regiao',
        'no_municipio',
        'no_uf',
    )

    list_filter = (
        'co_cr',
        'ds_cr',
        'no_regiao',
        'no_uf',
    )

    fields = list_display

class LimiteTerraIndigenaAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Admin model for LimiteTerraIndigenaAdmin."""

    def has_view_permission(self, request, obj=None):
        """
        Checks if the user has permission to view LimiteTerraIndigenaAdmin.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_funai_terras_indigenas' and perm_status:
                    return True
            
            return super().has_view_permission(request, obj)
        except Exception as e:
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
        Checks if the user has permission to change LimiteTerraIndigenaAdmin.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_funai_terras_indigenas' and perm_status:
                    return True

            return super().has_change_permission(request, obj)
        except Exception as e:
            print(f"Error checking change permission: {e}")
            return False 
         
    def has_add_permission(self, request):
        """
        Checks if the user has permission to add to LimiteTerraIndigenaAdmin.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_funai_terras_indigenas' and perm_status:
                    return True

            return super().has_add_permission(request)
        except Exception as e:
            print(f"Error checking add permission: {e}")
            return False    
        
    list_display = (
        'no_ti',
        'co_funai',
        'ds_fase_ti',
    )

    fields = list_display

    search_fields = (
        'no_ti',
        'co_funai',
    )

class InstrumentoGestaoFunaiAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Admin model for InstrumentoGestaoFunai."""

    def has_view_permission(self, request, obj=None):
        """
        Checks if the user has permission to view InstrumentoGestaoFunaiAdmin.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)
            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'visualizar_funai_instrumento_gestao' and perm_status:
                    return True
            
            return super().has_view_permission(request, obj)
        except Exception as e:
            print(f"Error checking view permission: {e}")
            return False    

    def has_change_permission(self, request, obj=None):
        """
        Checks if the user has permission to change InstrumentoGestaoFunaiAdmin.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'alterar_funai_instrumento_gestao' and perm_status:
                    return True

            return super().has_change_permission(request, obj)
        except Exception as e:
            print(f"Error checking change permission: {e}")
            return False 
         
    def has_add_permission(self, request):
        """
        Checks if the user has permission to add to InstrumentoGestaoFunaiAdmin.
        """
        try:
            current_user = request.user
            current_user_permissions, current_user_roles = get_user_permissions(current_user)

            for perm_name, perm_status in current_user_permissions:
                if perm_name == 'adicionar_funai_instrumento_gestao' and perm_status:
                    return True

            return super().has_add_permission(request)
        except Exception as e:
            print(f"Error checking add permission: {e}")
            return False    
        
    list_display = (
        'co_funai',
        'no_ti',
        'no_regiao',
        'sg_uf',
        'no_povo',
        'no_bioma',
        'ds_parceiros',
        'cr_funai',
        'no_ig',
        'ds_status',
        'nu_ano_elaboracao',
        'ds_disp_meio_local',
        'ds_tll_publi',
        'ds_obs',
        'dt_cadastro',
    )

    fields = list_display

    search_fields = (
        'no_ti',
        'co_funai',
        'no_regiao',
        'sg_uf',
    )

admin.site.register(models.CoordenacaoRegional, CoordenacaoRegionalAdmin)
admin.site.register(models.LimiteTerraIndigena, LimiteTerraIndigenaAdmin)
admin.site.register(models.InstrumentoGestaoFunai, InstrumentoGestaoFunaiAdmin)
