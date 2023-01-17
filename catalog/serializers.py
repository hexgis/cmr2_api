from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

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


class CatalogsSerializer(gis_serializers.GeoFeatureModelSerializer):
    """Serializer to return Catalogs scenes as GeoJSON compatible data."""
    class Meta:
        model = models.Catalogs
        geo_field = 'geom'
        fields = (
            "objectid",
            "image",
            "image_path",
            "url_tms",
            "date",
            "pr_date",
            "cloud_cover",
            "sat_id",
            "preview",
            "max_native_zoom",
            "type",
            "geom",
            "locator"
        )
