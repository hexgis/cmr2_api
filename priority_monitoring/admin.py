from django.contrib import admin

from priority_monitoring import models


class PriorityConsolidatedAdmin(admin.ModelAdmin):
    """PriorityConsolidatedAdmin model data."""

    list_display = (
        'id_tb',
        'no_estagio',
        'no_image',
        'dt_image',
        'nu_orbita',
        'nu_ponto',
        'dt_t0',
        'dt_t1',
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
        'no_cr',
        'no_ti',
    )

    fields = list_display

    search_fields = (
        'no_cr',
        'no_ti',
        'dt_t_um',
        'prioridade',
    )

    list_filter = (
        'no_cr',
        'no_ti',
        'prioridade',
    )


admin.site.register(
    models.PriorityConsolidated, PriorityConsolidatedAdmin)
