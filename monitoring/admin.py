from django.contrib import admin
from monitoring import models


class MonitoringConsolidatedAdmin(admin.ModelAdmin):
    """MonitoringConsolidatedAdmin model data."""

    list_display = (
        'id',
        'dt_t_um',
        'no_estagio',
        'nu_area_ha',
        'co_cr',
        'ds_cr',
        'co_funai',
        'no_ti',
    )

    fields = list_display

    search_fields = list_display


admin.site.register(models.MonitoringConsolidated, MonitoringConsolidatedAdmin)

