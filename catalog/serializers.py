from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

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


class CatalogsSerializer(GeoFeatureModelSerializer):
    
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
    #"""Atributo temporário até se implentado a paginação neste APP"""

       return getattr(obj, 'countt', 20)

    class Meta:

        model = models.Catalogs
        geo_field = 'geom'
        fields = (
            'geom',
            "objectid",
            "image",
            "type",
            "image_path",
            "url_tms",
            "date",
            "pr_date",
            "cloud_cover",
            "sat",
            "preview",
            "count",
            "max_native_zoom",
            "locator",
        )
