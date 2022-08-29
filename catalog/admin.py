from django.contrib import admin

from catalog import models


class SatteliteAdmin(admin.ModelAdmin):
    """Django Administrator `model.Sattelite` data."""

    list_display = (
        'identifier',
        'name',
        'description',
    )

    fields = list_display

    search_fields = list_display


admin.site.register(models.Sattelite, SatteliteAdmin)