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


class SceneAdmin(admin.GeoModelAdmin):
    """Django Administrator `model.Scene` data."""

    def cloud_cover_percent(self, instance:models.Scene)-> str:
        """_summary_

        Args:
            instance (models.Scene): Scene models data

        Returns:
            str: cloud cover in percent.
        """

        return '{}%'.format(instance.cloud_cover)

    list_display = (
        'image',
        'type',
        'date',
        'pr_date',
        'locator',
        'sat_identifier',
        'sat_name',
    )

    fields = (
        'image',
        'type',
        'image_path',
        'url_tms',
        'preview',
        'date',
        'cloud_cover_percent',
        'locator',
        'geom',
        'sat_identifier',
        'sat_name',
    )

    search_fields = ('image',)

    list_filter = ('date', )

    readonly_fields = fields


admin.site.register(models.Scene, SceneAdmin)
admin.site.register(models.Satellite, SatelliteAdmin)
