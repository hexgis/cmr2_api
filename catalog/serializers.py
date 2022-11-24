from rest_framework import serializers

from catalog import models


class SatelliteSerializer(serializers.ModelSerializer):
    """Serializer to return registered sattelites `models.Satellite` data."""

    class Meta:
        """Meta Class for `catalog.SatteliteSerializer` serializer."""
        model = models.Satellite
        fields = (
            'identifier',
            'name',
        )


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Catalog
        fields = "__all__"


# class Landsat8CatalogSerializer(serializers.ModelSerializer):
#     """Serializer to return `models.Landsat8Catalog` data."""
#     # satellite = SatteliteSerializer()
#     class Meta:
#         """Meta Class for `catalog.Landsat8CatalogSerializer` serializer."""
#         model = models.Landsat8Catalog
#         fields = "__all__"


# class Sentinel2CatalogSerializer(serializers.ModelSerializer):
#     """Serializer to return `models.Sentinel2Catalog` data."""
#     # satellite = SatteliteSerializer()

#     class Meta:
#         """Meta Class for `catalog.Sentinel2CatalogSerializer` serializer."""
#         model = models.Sentinel2Catalog
#         fields = "__all__"
