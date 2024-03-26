from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from support import models


class GeoserverSerializer(ModelSerializer):
    """GeoserverSerializer to serialize `models.Geoserver`."""

    class Meta:
        """Meta class for GeoserverSerializer."""

        model = models.Geoserver
        fields = (
            'name',
            'wms_url',
            'preview_url',
        )


class LayerFilterSerializer(ModelSerializer):
    """LayerFilterSerializer to serialize `models.LayerFilter`."""

    class Meta:
        """Meta class for LayerFilterSerializer."""

        model = models.LayerFilter
        fields = (
            'default',
            'filter_type',
            'label',
            'filter_alias',
        )


class WmsSerializer(ModelSerializer):
    """WmsSerializer to serialize `models.WmsLayer`."""

    geoserver = GeoserverSerializer()

    class Meta:
        """Meta class for WmsSerializer."""

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
    """TmsSerializer to serialize `models.TmsLayer`."""

    class Meta:
        """Meta class for TmsSerializer."""

        model = models.TmsLayer
        fields = (
            'url_tms',
            'date',
            'max_native_zoom',
        )


class LayersInfoSerializer(ModelSerializer):
    """LayersInfo to serialize `models.LayersGroup`."""
    class Meta:
        """Meta class for LayersInfo."""

        model = models.LayersInfo
        fields = '__all__'


class LayerSerializer(ModelSerializer):
    """LayerSerializer to serialize `models.Layer`."""

    tms = TmsSerializer()
    wms = WmsSerializer()
    layer_filters = LayerFilterSerializer(many=True)
    layers_info = LayersInfoSerializer()

    class Meta:
        """Meta class for LayerSerializer."""

        model = models.Layer
        fields = (
            'id',
            'tms',
            'wms',
            'layer_filters',
            'name',
            'order',
            'layer_type',
            'layers_info',
            'active_on_init',
            'is_public',
        )


class LayersGroupAuthenticatedSerializer(ModelSerializer):
    """LayersGroupAuthenticatedSerializer to serialize `models.LayersGroup`."""

    layers = LayerSerializer(many=True, read_only=True)

    class Meta:
        """Meta class for LayersGroupAuthenticatedSerializer."""

        model = models.LayersGroup
        fields = '__all__'


class LayersGroupPublicSerializer(ModelSerializer):
    """LayersGroupPublicSerializer to serialize `models.LayersGroup`."""

    layers = serializers.SerializerMethodField()

    class Meta:
        """Meta class for LayersGroupPublicSerializer."""

        model = models.LayersGroup
        fields = '__all__'

    def get_layers(self, obj):
        """Get layers from object.
        Args:
            obj (models.Layer): model instance.
        Returns:
            str: LayerSerializer.
        """

        public_layers = self.get_public_layer()
        serializer = LayerSerializer(
            data=public_layers.filter(layers_group=obj), many=True)
        serializer.is_valid()

        return serializer.data

    def get_public_layer(self):
        """Get layers from object.

        Args:
            obj (models.Layer): model instance.

        Returns:
            str: Layer object if is public.
        """

        return models.Layer.objects.filter(is_public=True)


class CategoryLayersGroupSerializer(ModelSerializer):
    """
    CategoryLayersGroupSerializer to serialize `models.CategoryLayersGroup`.
    """

    class Meta:
        """Meta class for CategoryLayersGroupSerializer."""
        model = models.CategoryLayersGroup
        fields = '__all__'


# class LayersInfoSerializer(ModelSerializer):
#     """LayersInfo to serialize `models.LayersGroup`."""
#     class Meta:
#         """Meta class for LayersInfo."""

#         model = models.LayersInfo
#         fields = '__all__'
