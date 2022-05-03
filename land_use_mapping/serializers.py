from django.db import models
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from land_use_mapping import models


class LandUseMappingGeomSerializer(gis_serializers.GeoFeatureModelSerializer):
    class Meta:
        geo_field = 'geom'
        field = '__all__'
        model = models.LandUseMappingClasses


class LandUseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LandUseMappingTI
        field = '__all__'
