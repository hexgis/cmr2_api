import base64
from django.db.models import Q

from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers


from layer import models


class GeoserverSerializer(serializers.ModelSerializer):
    """GeoserverSerializer to serialize `models.Geoserver`."""

    class Meta:
        """Meta class for GeoserverSerializer."""

        model = models.Geoserver
        fields = (
            'id',
            'name',
            'wms_url',
            'preview_url',
            'thumbnail_url',
            'geoserver_url',
        )


class TmsSerializer(serializers.ModelSerializer):
    """TmsSerializer to serialize `models.Tms`."""

    thumbnail_blob = serializers.SerializerMethodField()
    legend_blob = serializers.SerializerMethodField()

    def get_legend_blob(self, obj) -> str:
        """Get legend blob from object.

        Args:
            obj (models.Tms): model instance.

        Returns:
            str: Base64 encoded legend blob.
        """

        if not self.context.get('simple') and obj.legend_blob:
            return base64.b64encode(obj.legend_blob).decode('UTF-8')
        return None

    def get_thumbnail_blob(self, obj) -> str:
        """Get thumbnail blob from object.

        Args:
            obj (models.Tms): model instance.

        Returns:
            str: Base64 encoded thumbnail blob.
        """

        if not self.context.get('simple') and obj.thumbnail_blob:
            return base64.b64encode(obj.thumbnail_blob).decode('UTF-8')
        return None

    class Meta:
        """Meta class for TmsSerializer."""

        model = models.Tms
        fields = '__all__'


class WmsSerializer(serializers.ModelSerializer):
    """WmsSerializer to serialize `models.Wms`."""

    thumbnail_blob = serializers.SerializerMethodField()

    def get_thumbnail_blob(self, obj) -> str:
        """Get thumbnail blob from object.

        Args:
            obj (models.Wms): model instance.

        Returns:
            str: Base64 encoded thumbnail blob.
        """

        if 'request' in self.context.keys():
            data = self.context['request'].query_params.keys()
        else:
            data = self.context

        if (
                not 'simple' in data
                and obj.wms
                and obj.thumbnail_blob
        ):
            return base64.b64encode(obj.thumbnail_blob).decode('UTF-8')
        return None

    def to_representation(self, instance) -> dict:
        """Add Geoserver serialized data in WMS data representation.

        Args:
            instance (models.Wms): Object to be serialized.

        Returns:
            dict: WMS serialized result.
        """

        representation = super().to_representation(instance)
        serializer = GeoserverSerializer(instance.geoserver)
        representation['geoserver'] = serializer.data
        return representation

    class Meta:
        """Meta class for WmsSerializer."""

        model = models.Wms
        fields = '__all__'


class VectorSerializer(serializers.ModelSerializer):
    """VectorSerializer to serialize `models.Vector`."""

    def create(self, validated_data: dict) -> models.Vector:
        """Create a new vector instance.

        Args:
            validated_data (dict): Vector data.

        Returns:
            models.Vector: Vector instance.
        """

        return models.Vector.objects.create(**validated_data)

    class Meta:
        """Meta class for VectorSerializer."""

        model = models.Vector
        fields = '__all__'


class FilterSerializer(serializers.ModelSerializer):
    """FilterSerializer to serialize `models.Filter`."""

    def create(self, validated_data: dict) -> models.Filter:
        """Create a new filter instance.

        Args:
            validated_data (dict): Filter data.

        Returns:
            models.Filter: Filter instance.
        """

        del validated_data['layers']

        filter_obj = models.Filter.objects.create(**validated_data)

        data = self.context['request'].data

        if 'layers' in data:
            filter_obj.layers.clear()
            filter_obj.layers.set(data['layers'])

        return filter_obj

    def update(
        self,
        instance: models.Filter,
        validated_data: dict
    ) -> models.Filter:
        """Update filter instance.

        Args:
            instance (models.Filter): Filter instance.
            validated_data (dict): Validated data.

        Returns:
            models.Filter: Updated filter instance.
        """

        instance = super().update(instance, validated_data)

        data = self.context['request'].data

        if 'layers' in data:
            instance.layers.clear()
            instance.layers.set(data['layers'])

        instance.save()
        return instance

    class Meta:
        """Meta class for FilterSerializer."""

        model = models.Filter
        fields = '__all__'


class SimpleLayerSerializer(serializers.ModelSerializer):
    """SimpleLayerSerializer to serialize `models.Layer`."""

    class Meta:
        """Meta class for SimpleLayerSerializer."""

        model = models.Layer
        fields = ('id', 'name')


class LayerSerializer(serializers.ModelSerializer):
    """LayerSerializer to serialize `models.Layer`."""

    bbox = serializers.SerializerMethodField()
    wms = WmsSerializer(read_only=True)
    tms = TmsSerializer(read_only=True)
    vector = VectorSerializer(read_only=True)
    filters = FilterSerializer(many=True)
    group_name = serializers.SerializerMethodField()
    
    
    def __init__(self, *args, **kwargs):
        # Extracts `fields` from kwargs, if provided
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields:
            # Removes fields that are not in the `fields` list
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
                
    def get_bbox(self, obj) -> str:
        """Get bbox from object.

        Args:
            obj (models.Layer): model instance. 

        Returns:
            str: Bbox extent.
        """

        return obj.bbox.extent if obj.bbox else None
    
    def get_group_name(self, obj) -> str:
        """Get the name of the group related to the layer."""
        return obj.group.name if obj.group else None

    class Meta:
        """Meta class for LayerSerializer."""

        model = models.Layer
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """GroupSerializer to serialize `models.Group`."""

    layers = serializers.SerializerMethodField()

    def get_layers_id(self, obj: models.Layer) -> list:
        """Get layers from object.

        Args:
            obj (models.Layer): model instance.

        Returns:
            list: layers list.
        """

        if self.context['request'].user.is_anonymous:
            user_roles = []

        elif self.context['request'].user.is_admin():

            layers = models.Layer.objects.filter(group=obj)

            if 'initial' in self.context['request'].query_params.keys():
                layers = layers.filter(active_on_init=True)

            layer_list = [{"id": layer.id, "name": layer.name}
                          for layer in layers]
            return layer_list

        else:
            user_roles = self.context['request'].user.roles.all()

        # Verify if this group has any permitted or public layers
        layers = models.Layer.objects.filter(
            (
                Q(is_public=True) &
                Q(group=obj)
            ) | (
                Q(layer_permissions__groups__roles__in=user_roles) &
                Q(group=obj)
            )
        ).order_by('id').distinct('id')

        if 'initial' in self.context['request'].query_params.keys():
            layers = layers.filter(active_on_init=True)

        if layers.exists():
            layer_list = [{"id": layer.id, "name": layer.name}
                          for layer in layers]
            return layer_list
        else:
            return []

    class Meta:
        """Meta class for GroupSerializer."""

        model = models.Group
        fields = '__all__'


class GroupCompleteSerializer(serializers.ModelSerializer):
    """GroupSerializer to serialize `models.Group`."""

    layers = serializers.SerializerMethodField()

    def get_layers(self, obj: models.Group) -> list:
        """Get layers from object.

        Args:
            obj (models.Group): model instance.

        Returns:
            list: layers list.
        """

        if self.context['request'].user.is_anonymous:
            user_roles = []

        elif self.context['request'].user.is_admin():

            layers = models.Layer.objects.filter(group=obj)

            if 'initial' in self.context['request'].query_params.keys():
                layers = layers.filter(active_on_init=True)

            serializer = LayerSerializer(
                layers, many=True, context={'simple': True})
            return serializer.data

        else:
            user_roles = self.context['request'].user.roles.all()

        # Verify if this group has any permitted or public layers
        layers = models.Layer.objects.filter(
            (
                Q(is_public=True) &
                Q(group=obj)
            ) | (
                Q(layer_permissions__groups__roles__in=user_roles) &
                Q(group=obj)
            )
        ).order_by('id').distinct('id')

        if 'initial' in self.context['request'].query_params.keys():
            layers = layers.filter(active_on_init=True)

        if layers.exists():
            serializer = LayerSerializer(
                layers, many=True, context={'simple': True})
            return serializer.data

    class Meta:
        """Meta class for GroupSerializer."""

        model = models.Group
        fields = '__all__'


class GroupSimpleSerializer(serializers.ModelSerializer):
    """GroupSerializer to serialize `models.Group`."""

    class Meta:
        """Meta class for GroupSerializer."""

        model = models.Group
        fields = '__all__'


class BasemapSerializer(serializers.ModelSerializer):
    """BasemapSerializer to serialize `models.Basemap`."""

    class Meta:
        """Meta class for BasemapSerializer."""

        model = models.Basemap
        fields = '__all__'


class VectorGeometryListSerializer(gis_serializers.GeoFeatureModelSerializer):
    """Class to serialize `models.VectorGeometry` geo model data."""

    def to_representation(self, instance):
        """Custom representation to adjust the properties field."""

        obj = super().to_representation(instance)

        if 'properties' in self.context['request'].query_params.keys():
            obj['properties'] = obj['properties'].get('properties', {})

        return obj

    class Meta:
        """Meta class for `VectorGeometry`."""

        fields = ('id', 'properties',)
        id_field = False
        geo_field = 'geom'
        model = models.VectorGeometry


class VectorDetailSerializer(serializers.ModelSerializer):
    """Class to serialize `models.VectorGeometry` model data."""

    class Meta:
        """Meta class for `VectorDetailSerializer`."""

        model = models.VectorGeometry
        fields = (
            'id',
            'properties'
        )


class VectorGeometrySerializer(serializers.ModelSerializer):
    """Class to serialize `models.VectorGeometry` model data."""

    class Meta:
        """Meta class for `VectorDetailSerializer`."""

        fields = '__all__'
        model = models.VectorGeometry
