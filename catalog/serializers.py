from rest_framework import serializers

from catalog import models


class SatelliteSerializer(serializers.ModelSerializer):
    """Serializer to return registered sattelites `models.Satellite` data."""
    # satellite = SatteliteSerializer()

    class Meta:
        """Meta Class for `catalog.SatteliteSerializer` serializer."""
        model = models.Satellite
        fields = (
            'identifier',
            'name',
        )


class CatalogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Catalogs
        fields = "__all__"
