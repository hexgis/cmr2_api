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


class SceneSerializer(gis_serializers.GeoFeatureModelSerializer):
    """Serializer to return Scene scenes as GeoJSON compatible data."""

    srid = serializers.SerializerMethodField()

    def get_srid(self, instance:models.Scene)-> str:
        """_summary_

        Args:
            instance (models.Scene): Scene models data

        Returns:
            str: geometry srid code
        """

        return instance.geom.srid

    class Meta:
        """Meta Class for `catalog.SceneSerializer` serializer."""
        
        model = models.Scene
        geo_field = 'geom'
        fields = (
            'objectid',
            'image',
            'image_path',
            'url_tms',
            'date',
            'pr_date',
            'cloud_cover',
            'preview',
            'max_native_zoom',
            'type',
            'sat_identifier',
            'sat_name',
            'locator',
            'geom',
            'srid',
        )
