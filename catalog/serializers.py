from rest_framework import serializers

from catalog import models


class SatteliteSerializer(serializers.ModelSerializer):
    """Serializer to return registered sattelites."""

    class Meta:
        """Meta Class for `catalog.SatteliteSerializer` serializer."""
        model = models.Satellite
        fields = (
            'identifier',
            'name',
        )

class Landsat8CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Landsat8Catalog
        fields = "__all__"