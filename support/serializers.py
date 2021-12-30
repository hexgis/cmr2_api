from rest_framework.serializers import ModelSerializer

# from monitoring.serializers import MonitoringTypeSerializer

from support import models


class GeoserverSerializer(ModelSerializer):
    class Meta:
        model = models.Geoserver
        fields = (
            'name', 'wms_url', 'preview_url',
        )


# class LayerFilterSerializer(ModelSerializer):
#     class Meta:
#         model = models.LayerFilter
#         fields = (
#             'default', 'filter_type', 'label',
#         )


class WmsSerializer(ModelSerializer):
    geoserver = GeoserverSerializer()

    class Meta:
        model = models.WmsLayer
        fields = (
            'geoserver',
            'has_preview',
            'has_detail',
            'detail_width',
            'geoserver_layer_name',
            'geoserver_layer_namespace',
            'geoserver_layer_options',
            'has_opacity',
            'queryable',
            'default_opacity',
        )


class TmsSerializer(ModelSerializer):
    class Meta:
        model = models.TmsLayer
        fields = (
            'url_tms', 'date', 'max_native_zoom',
        )


# class HeatmapSerializer(ModelSerializer):
#     # heatmap_type = MonitoringTypeSerializer()

#     class Meta:
#         model = models.HeatmapLayer
#         # fields = ('heatmap_type', )
#         fields = (
#             'heatmap_type',
#         )


class LayerSerializer(ModelSerializer):
    tms = TmsSerializer()
    #heatmap = HeatmapSerializer()
    wms = WmsSerializer()
    # layer_filters = LayerFilterSerializer(many=True)

    class Meta:
        model = models.Layer
        fields = (
            'id',
            'tms',
            'wms',
            #'heatmap',
            # 'layer_filters',
            'name',
            'order',
            'layer_type',
            'active_on_init',
        )


class LayersGroupSerializer(ModelSerializer):
    layers = LayerSerializer(many=True, read_only=True)

    class Meta:
        model = models.LayersGroup
        fields = '__all__'
