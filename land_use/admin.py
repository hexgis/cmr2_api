from django.contrib import admin
from land_use import models
from cmr2_api.mixins import AdminPermissionMixin


class LandUseClassesAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Django administrator `models.LandUseClasses` data."""

    list_display = (
        'id',
        'sg_uf',
        'no_ti',
        'co_funai',
        'dt_homologada',
        'ds_cr',
        'co_cr',
        'nu_ano',
        'no_estagio',
        'no_satelites',
        'nu_resolucoes',
        'dt_imagens',
        'nu_area_km2',
        'nu_area_ha',
        'dt_cadastro',
    )

    fields = (
        'sg_uf',
        'no_ti',
        'co_funai',
        'dt_homologada',
        'ds_cr',
        'co_cr',
        'nu_ano',
        'no_estagio',
        'no_satelites',
        'nu_resolucoes',
        'dt_imagens',
        'nu_area_km2',
        'nu_area_ha',
        'dt_cadastro',
    )

    search_fields = (
        'id',
        'sg_uf',
        'no_ti',
        'co_funai',
        'ds_cr',
        'co_cr',
        'nu_ano',
        'no_estagio',
        'no_satelites',
        'nu_resolucoes',
    )
