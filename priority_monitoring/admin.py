from django.contrib import admin

from priority_monitoring import models


class PriorityConsolidatedAdmin(admin.ModelAdmin):
    """PriorityConsolidatedAdmin model data."""

    list_display = (
        'id_tb',
        'no_estagio',
        'no_imagem',
        'dt_imagem',
        'nu_orbita',
        'nu_ponto',
        'dt_t_zero ',
        'dt_t_um',
        'nu_area_km2',
        'nu_area_ha',
        'nu_latitude',
        'nu_longitude',
        'tempo',
        'contribuicao',
        'velocidade',
        'contiguidade',
        'ranking',
        'prioridade',
        'dt_cadastro',
        'ds_cr',
        'no_ti',
    )

    fields = list_display

    search_fields = (
        'ds_cr',
        'no_ti',
        'dt_t_um',
        'prioridade',
    )

    list_filter = (
        'ds_cr',
        'no_ti',
        'prioridade',
    )


admin.site.register(
    models.PriorityConsolidated, PriorityConsolidatedAdmin)
