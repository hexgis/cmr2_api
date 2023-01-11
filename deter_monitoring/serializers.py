from pyexpat import model
from attr import fields
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from deter_monitoring import models


class DeterDetailSerializer(serializers.ModelSerializer):
    """Serializer for `deter_monitoring.models.DeterTable` data."""

    class Meta:
        """Meta class for `DeterDetailSerializer` serializer."""
        model = models.DeterTable
        id_field = False
        fields = '__all__'


class DeterSerializer(gis_serializers.GeoFeatureModelSerializer):
    """Serializer for `deter_monitoring.models.DeterTable` data."""
    
    class Meta:
        """Meta class for `DeterSerializer` serializer."""
        model = models.DeterTable
        geo_field = 'geom'
        id_field = False
        fields = '__all__'


class DeterMapStatsSerializer(serializers.ModelField):
    """Serializer for `deter_monitoring.models.DeterTable` data."""

    class Meta:
        """Meta class for `DeterMapStatsSerializer` serializer."""
        model = models.DeterTable
        id_field = False
        fields = '__all__'


class DeterTableSerializer(serializers.ModelField):
    """Serializer for `deter_monitoring.models.DeterTable` data."""

    class Meta:
        """Meta class for `DeterTableSerializer` serializer."""
        model = models.DeterTable
        id_field = False
        exclude = 'geom'


class DeterTableStatsSerializer(serializers.ModelField):
    """Serializer for `deter_monitoring.models.DeterTable` data."""

    class Meta:
        """Meta class for `DeterTableStatsSerializer` serializer."""
        model = models.DeterTable
        id_field = False
        fields = '__all__'
        