from django.contrib import admin

from permission.mixins import Auth

from funai import models


class CoordenacaoRegionalAdmin(Auth, admin.ModelAdmin):
    """Admin model for CoordenacaoRegionalAdmin."""

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


class LimiteTerraIndigenaAdmin(Auth, admin.ModelAdmin):
    """Admin model for LimiteTerraIndigenaAdmin."""
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


class InstrumentoGestaoFunaiAdmin(Auth, admin.ModelAdmin):
    """Admin model for InstrumentoGestaoFunai."""

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
