from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from priority_alerts import models


class AlertsSerializers(gis_serializers.GeoFeatureModelSerializer):
    """Serializer for geographic `models.UrgentAlerts` spatial data."""
    class Meta:
        """Meta calss for geographic data `AlertsSerializers` serializer."""
        model = models.UrgentAlerts
        id_field = False
        geo_field = 'geom'
        fields = '__all__'


class AlertsTableSerializers(serializers.ModelSerializer):
    """Serializer to return data without geometry from `models.UrgentAlerts` data."""
    class Meta:
        """Meta class for `AlertsTableSerializers` serializer."""
        model = models.UrgentAlerts
        fields = '__all__'


class AlertsClassesSerializers(serializers.ModelSerializer):
    """Serializer to list classification stages adopted in mapping the 
    monitoring of indigenous land.
    """
    class Meta:
        """Meta class for `AlertsClassesSerializers` serializer."""
        model = models.UrgentAlerts
        fields = '__all__'
