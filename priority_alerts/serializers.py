from rest_framework import serializers

from rest_framework_gis import serializers as gis_serializers

from priority_alerts import models

import locale

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, 'pt_BR')


class AlertsSerializers(gis_serializers.GeoFeatureModelSerializer):
    """Serializer for geographic `models.UrgentAlerts` spatial data."""

    class Meta:
        """Meta calss for geographic data `AlertsSerializers` serializer."""
        model = models.UrgentAlerts
        id_field = False
        geo_field = 'geom'
        fields = (
            'id',
            'no_estagio',
            'nu_latitude',
            'nu_longitude',
        )


class AlertsTableSerializers(serializers.ModelSerializer):
    """Serializer to return data without geometry from `models.UrgentAlerts` 
    data."""

    nu_latitude = serializers.SerializerMethodField()
    nu_longitude = serializers.SerializerMethodField()
    nu_area_ha = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `AlertsTableSerializers` serializer."""
        model = models.UrgentAlerts
        fields = (
            'id',
            'no_ciclo',
            'no_titulo',
            'no_arquivo',
            'nu_referencia',
            'nu_mapa',
            'no_estagio',
            'no_imagem',
            'nu_orbita_ponto',
            'dt_t_zero',
            'dt_t_um',
            'nu_area_ha',
            'co_funai',
            'no_ti',
            'co_cr',
            'ds_cr',
            'no_municipio',
            'sg_uf',
            'nu_longitude',
            'nu_latitude',
        )

    def format_area(self, value):
        return locale.format_string("%.3f", value, grouping=True)

    def format_coord(self, value):
        return locale.format_string("%.6f", value, grouping=True)

    def get_nu_area_ha(self, obj):
        return self.format_area(obj.nu_area_ha)

    def get_nu_latitude(self, obj):
        return self.format_coord(obj.nu_latitude)

    def get_nu_longitude(self, obj):
        return self.format_coord(obj.nu_longitude)


class AlertsDetailSerializers(serializers.ModelSerializer):
    """Serializer to return detailed `models.UrgentAlerts` data."""

    class Meta:
        """Meta class for `AlertsDetailSerializers` serializer."""
        model = models.UrgentAlerts
        fields = (
            'id',
            'co_funai',
            'no_ti',
            'ds_cr',
            'nu_referencia',
            'no_estagio',
            'no_imagem',
            'dt_t_zero',
            'dt_t_um',
            'nu_area_ha',
            'nu_longitude',
            'nu_latitude',
            'no_municipio',
            'sg_uf',
        )


class AlertsClassesSerializers(serializers.ModelSerializer):
    """Serializer to list classification stages adopted in mapping the 
    monitoring of indigenous land.
    """

    class Meta:
        """Meta class for `AlertsClassesSerializers` serializer."""
        model = models.UrgentAlerts
        fields = (
            'no_estagio',
        )
