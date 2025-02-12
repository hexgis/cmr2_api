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


class LandUseDetailSerializer(serializers.ModelSerializer):
    """Serializer for return detailed `models.LandUseClasses` data."""

    class Meta:
        """Meta class for `LandUseDetailSerializer` serializer."""
        model = models.LandUseClasses
        fields = (
            'co_funai',
            'no_ti',
            'ds_cr',
            'sg_uf',
            'no_estagio',
            'no_satelites',
            'dt_imagens',
            'nu_area_ha',
        )

class LandUseToCompareSerializer(serializers.ModelSerializer):
    """Serializer to return model from `models.LandUseClasses` data.
    
    Serializes model data to return table info without geometry.
    """

    class Meta:
        """Meta class for `LandUseTableSerializer` serializer."""
        model = models.LandUseClasses
        fields = (
            'ds_cr',
            'co_cr',
            'no_ti',
            'co_funai',
        )

class LandUseCrSerializer(serializers.ModelSerializer):
    """Serializer to return model from `models.LandUseClasses` data.
    
    Serializes model data to return table info without geometry.
    """
    co_cr = serializers.CharField(source='cr_co_cr')
    ds_cr = serializers.CharField(source='cr_no_cr')
    no_regiao = serializers.CharField(source='cr_no_regiao')

    class Meta:
        """Meta class for `LandUseTableSerializer` serializer."""
        model = models.LandUseVmRegionalCoordnation
        fields = (
            'no_regiao',
            'ds_cr',
            'co_cr',
        )

class LandUseTiSerializer(serializers.ModelSerializer):
    """Serializer to return model from `models.LandUseClasses` data.
    
    Serializes model data to return table info without geometry.
    """
    no_ti = serializers.CharField(source='ti_no_ti')
    co_funai = serializers.CharField(source='ti_co_funai')
    co_cr = serializers.CharField(source='cr_co_cr')

    class Meta:
        """Meta class for `LandUseTableSerializer` serializer."""
        model = models.LandUseClasses
        fields = (
            'no_ti',
            'co_funai',
            'co_cr'
        )

class LandUseTesteSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class for `LandUseTableSerializer` serializer."""
        model = models.LandUseVmRegionalCoordnation
        fields = "__all__"
