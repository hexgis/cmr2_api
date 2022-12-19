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
    satellite = serializers.SerializerMethodField()
    # satellite2 = SatelliteSerializer()
    def get_satellite(sefl, obj):

        return obj.sat.name

    class Meta:
        model = models.Catalogs
        # fields = "__all__"
        fields = (
            "objectid",
            "image",
            "type",
            "image_path",
            "url_tms",
            "date",
            "pr_date",
            "cloud_cover",
            "sat",
            "satellite",
            "preview",
            # "satellite2",
        )
        geo_field = 'geom'