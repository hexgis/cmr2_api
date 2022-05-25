from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from priority_alerts import models


class AlertsSerializers(gis_serializers.GeoFeatureModelSerializer):
    """Serializer..."""
    class Meta:
        """Meta class for..."""
        model = models.UrgentAlerts
        id_field = False
        geo_field = 'geom'
        fields = '__all__'


class AlertsTableSerializers(serializers.ModelField):
    """Serializer..."""
    class Meta:
        """Meta class for..."""
        model = models.UrgentAlerts
        exclude = ['geom']


class AlertsDetailSerializers(serializers.ModelField):
    """Serializer..."""
    class Meta:
        """Meta class for..."""
        model = models.UrgentAlerts
        fields = '__all__'


class AlertsStatsSerializers(serializers.ModelField):
    """Serializer..."""
    class Meta:
        """Meta class for..."""
        model = models.UrgentAlerts
        fields = '__all__'


class AlertsClassesSerializers(serializers.ModelField):
    """Serializer..."""
    class Meta:
        """Meta class for..."""
        model = models.UrgentAlerts
        fields = '__all__'
