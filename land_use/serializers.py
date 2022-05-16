from django.db import models
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from land_use import models


class LandUseSerializer(gis_serializers.GeoFeatureModelSerializer):
    """Serializer for geographic `models.LandUseClasses` spatial data."""
    class Meta:
        """Meta calss for geographic data `LandUseSerializer` serializer."""
        model = models.LandUseClasses
        id_field = False
        geo_field = 'geom'
        fields = (
            'id',
            'nu_latitude',
            'nu_longitude',
        )


class LandUseDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed `models.LandUseClasses` data."""
    class Meta:
        """Meta class for `LandUseDetailSerializer` serializer."""
        model = models.LandUseClasses
        id_field = False
        fields = (
            'id',
            'sg_uf',
            'no_ti',
            'co_funai',
            'dt_homologada',
            'ds_cr',
            'co_cr',
            'nu_ano',
            'no_estagio',
            'no_satelites',
            'nu_resolucoes',
            'dt_imagens',
            'nu_area_km2',
            'nu_area_ha',
            'dt_cadastro',
        )


class LandUseYearsSerializer(serializers.ModelSerializer):
    """Serializer to list years with land use mapping 'models.LandUseClasses' data."""
    class Meta:
        """Meta class for 'LandUseYearsSerializer' serializer."""
        model = models.LandUseClasses
        id_field = False
        fields = ('nu_ano',)


class LandUseTableSerializer(serializers.ModelSerializer):
    """Serializer to return data without geometry from 'models.LandUseClasses' data."""
    class Meta:
        """Meta class for 'LandUseTableSerializer' serializer."""
        model = models.LandUseClasses
        id_field = False
        fields = (
            'id',
            'sg_uf',
            'no_ti',
            'co_funai',
            'dt_homologada',
            'ds_cr',
            'co_cr',
            'nu_ano',
            'no_estagio',
            'no_satelites',
            'nu_resolucoes',
            'dt_imagens',
            'nu_area_km2',
            'nu_area_ha',
            'dt_cadastro',
        )


class LandUseClassesSerializer(serializers.ModelSerializer):
    """Serializer to list classification stages adopted in land use mapping 'models.LandUseClasses' data."""
    class Meta:
        """Meta class for 'LandUseClassesSerializer' serializer."""
        model = models.LandUseClasses
        id_field = False
        fields = ('no_estagio',)
