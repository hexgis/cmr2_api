from django.contrib import admin

from catalog import models


class SatelliteAdmin(admin.ModelAdmin):
    """Django Administrator `model.Satellite` data."""

    list_display = (
        'identifier',
        'name',
        'description',
    )

    fields = list_display

    search_fields = list_display

admin.site.register(models.Satellite, SatelliteAdmin)
