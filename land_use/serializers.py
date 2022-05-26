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
            'no_estagio',
            'nu_latitude',
            'nu_longitude',
        )


class LandUseYearsSerializer(serializers.ModelSerializer):
    """Serializer to list years from `models.LandUseClasses` data.

    Serializes model data to return list of years with land use mapping
    """

    class Meta:
        """Meta class for `LandUseYearsSerializer` serializer."""
        model = models.LandUseClasses
        id_field = False
        fields = ('nu_ano',)


class LandUseTableSerializer(serializers.ModelSerializer):
    """Serializer to return model from `models.LandUseClasses` data.
    
    Serializes model data to return table info without geometry.
    """

    class Meta:
        """Meta class for `LandUseTableSerializer` serializer."""
        model = models.LandUseClasses
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
    """Serializer to list classification stages adopted in land use mapping 
    'models.LandUseClasses' data.
    """

    class Meta:
        """Meta class for `LandUseClassesSerializer` serializer."""
        model = models.LandUseClasses
        id_field = False
        fields = ('no_estagio',)
