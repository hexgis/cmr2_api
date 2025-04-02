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
