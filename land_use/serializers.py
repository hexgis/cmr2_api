from django.db import models
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from land_use import models
from django.db.models import Q

# Importando do utils
from utils.format_values import format_area, format_coord, format_date

# Lista de campos de área e coordenadas (mantidas iguais)
AREA_FIELDS = [
    'nu_area_ag_ha', 'nu_area_cr_ha', 'nu_area_dg_ha', 'nu_area_ma_ha',
    'nu_area_no_ha', 'nu_area_rv_ha', 'nu_area_sv_ha', 'nu_area_vi_ha',
    'nu_area_vn_ha', 'nu_area_mi_ha', 'nu_area_ha', 'nu_area_km2',
]

COORD_FIELDS = ['nu_latitude', 'nu_longitude']


class LandUseSerializer(gis_serializers.GeoFeatureModelSerializer):
    """Serializer for geographic `models.LandUseClasses` spatial data."""
    nu_latitude = serializers.SerializerMethodField()
    nu_longitude = serializers.SerializerMethodField()

    class Meta:
        """Meta class for geographic data `LandUseSerializer` serializer."""
        model = models.LandUseClasses
        id_field = False
        geo_field = 'geom'
        fields = (
            'id',
            'no_estagio',
            'nu_latitude',
            'nu_longitude',
        )

    def get_nu_latitude(self, obj):
        return format_coord(obj.nu_latitude)

    def get_nu_longitude(self, obj):
        return format_coord(obj.nu_longitude)


class LandUseTableSerializer(serializers.ModelSerializer):
    """Serializer for return data from model `LandUsePerTi`."""

    # Definindo os campos dinamicamente como SerializerMethodField
    for field in AREA_FIELDS:
        locals()[field] = serializers.SerializerMethodField()

    for field in COORD_FIELDS:
        locals()[field] = serializers.SerializerMethodField()

    # Adicionando campo de data formatada
    dt_imagens = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `LandUseTableSerializer`."""
        model = models.LandUsePerTi
        fields = [
            'id', 'sg_uf', 'no_ti', 'co_funai', 'co_cr', 'dt_homologada', 'ds_cr',
            'nu_ano', 'no_satelites', 'nu_resolucoes', 'dt_imagens',
        ] + AREA_FIELDS + COORD_FIELDS

    def get_field_value(self, obj, field):
        """Retorna o valor formatado baseado no tipo do campo."""
        value = getattr(obj, field, None)
        if field in AREA_FIELDS:
            return format_area(value)
        elif field in COORD_FIELDS:
            return format_coord(value)
        elif field == 'dt_imagens':  # Tratamento específico para data
            return format_date(value)
        return value

    def __getattr__(self, name):
        if name.startswith('get_') and name[4:] in AREA_FIELDS + COORD_FIELDS + ['dt_imagens']:
            field = name[4:]
            return lambda obj: self.get_field_value(obj, field)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")


class LandUseDetailSerializer(serializers.ModelSerializer):
    """Serializer for return detailed `models.LandUseClasses` data."""
    nu_area_ha = serializers.SerializerMethodField()
    dt_imagens = serializers.SerializerMethodField()

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

    def get_nu_area_ha(self, obj):
        return format_area(obj.nu_area_ha)

    def get_dt_imagens(self, obj):
        return format_date(obj.dt_imagens)


class LandUseSearchSerializer(serializers.ModelSerializer):
    """Serializer para busca em LandUseVmRegionalCoordnation."""

    cr_no_regiao = serializers.SerializerMethodField()

    class Meta:
        model = models.LandUsePerTi
        fields = [
            'co_funai',
            'co_cr',
            'nu_ano',
            'ds_cr',
            'no_ti',
            'cr_no_regiao',  # Adicionando campo calculado
        ]

    def get_cr_no_regiao(self, obj):
        from land_use.models import LandUseVmRegionalCoordnation

        regiao = LandUseVmRegionalCoordnation.objects.filter(
            Q(ti_co_funai=str(obj.co_funai)) | Q(
                cr_co_cr=str(obj.co_cr))
        ).first()

        if regiao:
            return regiao.cr_no_regiao
        return None
