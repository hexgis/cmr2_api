from django.db import models
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from land_use import models


class LandUseGeomSerializer(gis_serializers.GeoFeatureModelSerializer):
    class Meta:
        geo_field = 'geom'
        field = '__all__'
        model = models.LandUseClasses


class LandUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LandUseTI
        field = '__all__'
