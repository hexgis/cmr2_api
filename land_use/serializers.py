from django.db import models

from rest_framework import serializers

from rest_framework_gis import serializers as gis_serializers

from land_use import models

import locale

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, 'pt_BR')



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

AREA_FIELDS = [
    'nu_area_ag_ha', 'nu_area_cr_ha', 'nu_area_dg_ha', 'nu_area_ma_ha',
    'nu_area_no_ha', 'nu_area_rv_ha', 'nu_area_sv_ha', 'nu_area_vi_ha',
    'nu_area_vn_ha', 'nu_area_mi_ha', 'nu_area_ha', 'nu_area_km2',
]

COORD_FIELDS = ['nu_latitude', 'nu_longitude']

class FormatFieldsMixin:
    """Mixin for format field."""
    
    def format_area(self, value):
        return locale.format_string("%.3f", value, grouping=True) if value is not None else None

    def format_coord(self, value):
        return locale.format_string("%.6f", value, grouping=True) if value is not None else None


class LandUseTableSerializer(serializers.ModelSerializer, FormatFieldsMixin):
    """ Serializer for return data from model `LandUsePerTi` """

    for field in AREA_FIELDS:
        locals()[field] = serializers.SerializerMethodField()

    for field in COORD_FIELDS:
        locals()[field] = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `LandUseTableSerializer`."""
        model = models.LandUsePerTi
        fields = [
            'id', 'sg_uf', 'no_ti', 'co_funai', 'co_cr', 'dt_homologada', 'ds_cr',
            'nu_ano', 'no_satelites', 'nu_resolucoes', 'dt_imagens',
        ] + AREA_FIELDS + COORD_FIELDS

    def get_field_value(self, obj, field):
        """Return formated value based on field type."""
        value = getattr(obj, field, None)
        if field in AREA_FIELDS:
            return self.format_area(value)
        elif field in COORD_FIELDS:
            return self.format_coord(value)
        return value

    def __getattr__(self, name):
        if name.startswith('get_') and name[4:] in AREA_FIELDS + COORD_FIELDS:
            field = name[4:]
            return lambda obj: self.get_field_value(obj, field)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


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

class LandUseSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LandUsePerTi
        fields = ['co_funai','co_cr','nu_ano', 'ds_cr', 'no_ti']
