from django.contrib import admin
from deter_monitoring import models

class DeterTIAdmin(admin.ModelAdmin):
    """Django administrator `models.DeterTI` data."""

    list_display = (
        'ds_cr',
        'no_ti',
        'classname',
        'quadrant',
        'path_row',
        'areatotalkm',
        'view_date',
        'sensor',
        'satellite',
        'uf',
        'municipality',
        'uc',
    )

    field = list_display

    search_fields = list_display


admin.site.register(models.DeterTI, DeterTIAdmin)