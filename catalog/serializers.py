from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

import os
from django.conf import settings

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
    preview = serializers.SerializerMethodField()
    image_path = serializers.SerializerMethodField()

    def get_preview(self, instance):
        if instance.preview is not None:
            return os.path.join(settings.DOMAIN_API, instance.preview)
        else:
            return "URL não encontrada"

    def get_image_path(self, instance):
        if instance.image_path is not None:
            url_catalog = instance.image_path.replace('\\','/').replace(
                "//hex-funai.hex.com/", '').replace("media/", '')
            url_catalog = os.path.join(settings.DOMAIN_API, url_catalog)
            return url_catalog
        else:
            return "URL não encontrada"

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
            "preview",
            "max_native_zoom",
            "type",
            "sat_identifier",
            "sat_name",
            "locator",
            "geom",
        )