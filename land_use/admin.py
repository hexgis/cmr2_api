from django.contrib import admin
from land_use import models


class LandUseClassesAdmin(admin.ModelAdmin):
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


class LandUseTIAdmin(admin.ModelAdmin):
    """Django administrator `models.LandUseTi` data."""

    list_display = (
        'id',
        'sg_uf',
        'no_ti',
        'co_funai',
        'dt_homologada',
        'ds_cr',
        'co_cr',
        'nu_ano',
        'no_satelites',
        'nu_resolucoes',
        'dt_imagens',
        'nu_area_ag_ha',
        'nu_area_cr_ha',
        'nu_area_dg_ha',
        'nu_area_ma_ha',
        'nu_area_no_ha',
        'nu_area_rv_ha',
        'nu_area_sv_ha',
        'nu_area_vi_ha',
        'nu_area_vn_ha',
        'nu_area_mi_ha',
        'nu_area_ha',
        'nu_area_km2',
    )
    fields = (
        'sg_uf',
        'no_ti',
        'co_funai',
        'dt_homologada',
        'ds_cr',
        'co_cr',
        'nu_ano',
        'no_satelites',
        'nu_resolucoes',
        'dt_imagens',
        'nu_area_ag_ha',
        'nu_area_cr_ha',
        'nu_area_dg_ha',
        'nu_area_ma_ha',
        'nu_area_no_ha',
        'nu_area_rv_ha',
        'nu_area_sv_ha',
        'nu_area_vi_ha',
        'nu_area_vn_ha',
        'nu_area_mi_ha',
        'nu_area_ha',
        'nu_area_km2',
    )

    search_fields = (
        'id',
        'sg_uf',
        'no_ti',
        'co_funai',
        'ds_cr',
        'co_cr',
        'nu_ano',
        'no_satelites',
        'nu_resolucoes',
    )


admin.site.register(models.LandUseClasses, LandUseClassesAdmin)
admin.site.register(models.LandUseTI, LandUseTIAdmin)
