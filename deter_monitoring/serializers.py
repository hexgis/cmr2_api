from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from deter_monitoring import models


class DeterTIDetailSerializer(serializers.ModelSerializer):
    """Serializer for `deter_monitoring.models.DeterTI` data."""

    class Meta:
        """Meta class for `DeterDetailSerializer` serializer."""
        model = models.DeterTI
        id_field = False
        exclude = ['geom', ]


class DeterTISerializer(gis_serializers.GeoFeatureModelSerializer):
    """Serializer for `deter_monitoring.models.DeterTI` data."""

    class Meta:
        """Meta class for `DeterSerializer` serializer."""
        model = models.DeterTI
        geo_field = 'geom'
        id_field = False
        fields = '__all__'


class DeterTIMapStatsSerializer(serializers.ModelSerializer):
    """Serializer for `deter_monitoring.models.DeterTI` data."""

    class Meta:
        """Meta class for `DeterMapStatsSerializer` serializer."""
        model = models.DeterTI
        id_field = False
        fields = ['area_total_km', ]


class DeterTITableSerializer(serializers.ModelSerializer):
    """Serializer for `deter_monitoring.models.DeterTI` data."""

    class Meta:
        """Meta class for `DeterTISerializer` serializer."""
        model = models.DeterTI
        id_field = False
        exclude = ['geom', ]


class DeterTITableStatsSerializer(serializers.ModelSerializer):
    """Serializer for `deter_monitoring.models.DeterTI` data."""

    class Meta:
        """Meta class for `DeterTIStatsSerializer` serializer."""
        model = models.DeterTI
        id_field = False
        exclude = ['geom', ]
