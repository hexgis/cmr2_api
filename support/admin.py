from django.contrib import admin

from support import models


class GeoserverAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'wms_url',
        'preview_url',
    )
    fields = list_display
    search_fields = list_display


class CategoryLayersGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'icon',
        'description'
    )
    fileds = list_display
    search_fields = list_display


class LayersGroupAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'order',
        'category_groups'
    )
    fields = list_display
    search_fields = list_display


class LayerAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'order',
        'layer_type',
        'active_on_init',
        'layers_group',
        'is_public',
    )

    fields = list_display
    search_fields = (
        'name',
        'layers_group__name',
    )

    list_filter = (
        'layer_type',
        'is_public',
    )


class WmsLayerAdmin(admin.ModelAdmin):

    list_display = (
        'layer',
        'geoserver_layer_name',
        'geoserver_layer_namespace',
        'geoserver',
        'has_preview',
        'has_detail',
        'detail_width',
    )

    fields = (
        'layer',
        'geoserver_layer_name',
        'geoserver_layer_namespace',
        'geoserver',
        'geoserver_layer_options',
        'has_preview',
        'has_detail',
        'detail_width',
        'has_opacity',
        'queryable',
        'default_opacity',
    )
    search_fields = (
        'geoserver_layer_name',
        'geoserver_layer_namespace',
    )

    list_filter = (
        'geoserver',
        'has_preview',
        'has_detail',
        'geoserver_layer_namespace',
    )
    list_per_page = 25


class TmsLayerAdmin(admin.ModelAdmin):

    list_display = (
        'layer',
        'url_tms',
        'date',
        'max_native_zoom',
    )

    fields = list_display

    search_field = (
        'date',
    )

    list_filter = (
        'max_native_zoom',
    )


class LayerFilterAdmin(admin.ModelAdmin):

    list_display = (
        'label',
        'default',
        'filter_type',
        'filter_alias',
    )

    fields = (
        'default',
        'filter_type',
        'label',
        'layers',
        'filter_alias',
    )

    list_filter = (
        'filter_alias',
        'filter_type',
    )


admin.site.register(models.Geoserver, GeoserverAdmin)
admin.site.register(models.LayersGroup, LayersGroupAdmin)
admin.site.register(models.Layer, LayerAdmin)
admin.site.register(models.WmsLayer, WmsLayerAdmin)
admin.site.register(models.TmsLayer, TmsLayerAdmin)
admin.site.register(models.CategoryLayersGroup, CategoryLayersGroupAdmin)
admin.site.register(models.LayerFilter, LayerFilterAdmin)
