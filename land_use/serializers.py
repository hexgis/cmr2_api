from decimal import Clamped
from pyexpat import model
from django.db import models
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from land_use import models


class LandUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LandUseClasses
        id_field = False  # perguntar para o Naldo
        field = '__all__'


class LandUseGeomSerializer(gis_serializers.GeoFeatureModelSerializer):
    class Meta:
        model = models.LandUseClasses
        id_field = False
        geo_field = 'geom'
        field = '__all__'


class LandUseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LandUseClasses
        field = '__all__'


class LandUseYearsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LandUseClasses
        field = '__all__'
