from django.contrib import admin

from .models import (
    Geoserver,
    LayersGroup,
    Layer,
    WmsLayer,
    TmsLayer
    #HeatmapLayer
    # LayerFilter
)


class GeoserverAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'wms_url',
        'preview_url',
    )
    fields = list_display
    search_fields = list_display


class LayersGroupAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'order',
        'icon',
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
    )

    fields = list_display
    search_fields = (
        'name',
        'layers_group__name',
    )

    list_filter = (
        'layer_type',
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
    list_per_page=25

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


# class HeatmapLayerAdmin(admin.ModelAdmin):

#     list_display = (
#         #'layer',
#         'heatmap_type',
#     )

#     fields = list_display

#     list_filter = (
#         'heatmap_type',
#     )


# class LayerFilterAdmin(admin.ModelAdmin):

#     list_display = (
#         'label',
#         'default',
#         'filter_type',
#     )

#     fields = (
#         'default',
#         'filter_type',
#         'label',
#         'layers',
#     )

#     list_filter = (
#         'filter_type',
#     )


admin.site.register(Geoserver, GeoserverAdmin)
admin.site.register(LayersGroup, LayersGroupAdmin)
admin.site.register(Layer, LayerAdmin)
admin.site.register(WmsLayer, WmsLayerAdmin)
admin.site.register(TmsLayer, TmsLayerAdmin)
# admin.site.register(HeatmapLayer, HeatmapLayerAdmin)
# admin.site.register(LayerFilter, LayerFilterAdmin)
