from django.contrib.gis import admin

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

    readonly_fields = fields


class CatalogsAdmin(admin.GeoModelAdmin):
    """Django Administrator `model.Catalogs` data."""
    def cloud_cover_percent(self, instance):
        return '{}%'.format(instance.cloud_cover)

    list_display = (
        'image',
        'type',
        'date',
        'pr_date',
        'locator',
        'sat'
    )

    fields = (
        'image',
        'type',
        'image_path',
        'url_tms',
        'date',
        # 'pr_date',
        'cloud_cover_percent',
        'locator',
        'geom',
        'sat'
    )

    search_fields = ('image',)

    list_filter = ('date', )

    readonly_fields = fields


admin.site.register(models.Catalogs, CatalogsAdmin)
admin.site.register(models.Satellite, SatelliteAdmin)