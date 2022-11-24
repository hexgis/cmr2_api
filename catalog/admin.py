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


class CatalogAdmin(admin.GeoModelAdmin):
    """Django Administrator `model.Catalog` data."""
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


# class Landsat8CatalogAdmin(admin.GeoModelAdmin):
#     """Django Administrator `model.Landsat8Catalog` data."""

#     list_display = (
#         'id',
#         'pk',
#         'image',
#         'satellite',
#         'type',
#         'date',
#         'orbita',
#         'ponto',
#     )

#     fields = (
#         'image',
#         'satellite',
#         'type',
#         'path',
#         'url_tms',
#         'date',
#         'cloud_cover',
#         'orbita',
#         'ponto',
#         'geom',
#         'max_native_zoom',
#     )

#     search_fields = list_display


# class Sentinel2CatalogAdmin(admin.GeoModelAdmin):
#     """Django Administrator `model.Sentinel2Catalog` data."""

#     # def tile(self, instance):
#     #     return "{}{}{}".format(instance.utm_zone,
#     #                            instance.latitude_band, instance.grid_square)

#     list_display = (
#         'id',
#         'pk',
#         'image',
#         'satellite',
#         'type',
#         'date',
#         'utm_zone',
#         #'tile',
#     )

#     fields = (
#         'image',
#         'satellite',
#         'type',
#         'path',
#         'url_tms',
#         'date',
#         'cloud_cover',
#         # 'tile',
#         'geom',
#         'max_native_zoom',
#     )

#     search_fields = list_display


admin.site.register(models.Catalog, CatalogAdmin)
admin.site.register(models.Satellite, SatelliteAdmin)
# admin.site.register(models.Landsat8Catalog, Landsat8CatalogAdmin)
# admin.site.register(models.Sentinel2Catalog, Sentinel2CatalogAdmin)
