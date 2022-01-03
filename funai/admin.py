from django.contrib import admin

from funai import models

class CoordenacaoRegionalAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        # 'co_cr',
        'no_cr',
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
    fields = list_display
    search_fields = (
        # 'co_cr',
        'no_cr',
        'no_regiao',
        'no_municipio',
        'no_uf',
    )
    list_fielter = (
        # 'co_cr',
        'no_cr',
        'no_regiao',
        'no_uf',
    )

class LimiteTerraIndigenaAdmin(admin.ModelAdmin):
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

admin.site.register(models.CoordenacaoRegional, CoordenacaoRegionalAdmin)
admin.site.register(models.LimiteTerraIndigena, LimiteTerraIndigenaAdmin)
