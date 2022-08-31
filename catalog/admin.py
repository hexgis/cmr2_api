# from django.contrib import admin
from django.contrib.gis import admin

from catalog import models


class SatteliteAdmin(admin.ModelAdmin):
    """Django Administrator `model.Satellite` data."""

    list_display = (
        'identifier',
        'name',
        'description',
    )

    fields = list_display

    search_fields = list_display


class Landsat8CatalogAdmin(admin.ModelAdmin):
    """Django Administrator `model.Landsat8Catalog` data."""
    # list_display = [field.name for field in models.Landsat8Catalog._meta.get_fields()]
    list_display = (
        'image',
        'satellite',
        'type',
        'date',
        'orbita',
        'ponto',
    )

    fields = (
        'image',
        'satellite',
        'type',
        'path',
        'url_tms',
        'date',
        'cloud_cover',
        'orbita',
        'ponto',
        # 'geom',
        'max_native_zoom',
    )

    search_fields = list_display


class Sentinel2CatalogAdmin(admin.ModelAdmin):
    """Django Administrator `model.Sentinel2Catalog` data."""
    def tile(self, instance):
        return "{}{}{}".format(instance.utm_zone,
                               instance.latitude_band, instance.grid_square)

    # list_display = [field.name for field in models.Sentinel2Catalog._meta.get_fields()]
    list_display = (
        'image',
        'satellite',
        'type',
        'date',
        'utm_zone',#'tile',
    )

    fields = (
        'image',
        'satellite',
        'type',
        'path',
        'url_tms',
        'date',
        'cloud_cover',
        'tile',
        # 'geom',
        'max_native_zoom',
    )

    search_fields = list_display


admin.site.register(models.Satellite, SatteliteAdmin)
admin.site.register(models.Landsat8Catalog, Landsat8CatalogAdmin)
admin.site.register(models.Sentinel2Catalog, Sentinel2CatalogAdmin)