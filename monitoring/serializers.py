from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from monitoring import models


class MonitoringConsolidatedSerializer(gis_serializers.GeoFeatureModelSerializer):
    """Serializer for `models.MonitoringConsolidated` data."""
    class Meta:
        """Meta class for `MonitoringConsolidatedSerializer` serializer."""
        model = models.MonitoringConsolidated
        geo_field = 'geom'
        id_field = False
        fields = (
            'id',
            'no_imagem',
            'dt_imagem',
            'no_estagio',
            'nu_orbita',
            'nu_ponto',
            'nu_latitude',
            'nu_longitude',
            'dt_t_zero',
            'dt_t_um',
            'co_funai',
            'nu_area_km2',
            'nu_area_ha',
            'co_cr',
            'ds_cr',
            'no_ti',
            'ti_nu_area_ha',
            'geom',
        )


class MonitoringConsolidatedDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed `models.MonitoringConsolidated` data."""

    class Meta:
        """Meta class for `MonitoringConsolidatedDetailSerializer` serializer."""
        model = models.MonitoringConsolidated
        id_field = False
        fields = (
            'co_funai',
            'no_ti',
            'ds_cr',
            'no_estagio',
            'no_imagem',
            'dt_t_zero',
            'dt_t_um',
            'nu_area_ha',
            'nu_latitude',
            'nu_longitude',
            'ti_nu_area_ha',
        )


class MonitoringConsolidatedClassesSerializer(serializers.ModelSerializer):
    """Serializer for stages 'MonitoringConsolidatedClassesSerializer' data."""

    def to_representation(self, instance) -> str:
        """Representates model data instance as simple string.

        Returns:
            str: abbreviation of types stages
        """
        return f'{instance.no_estagio}'

    class Meta:
        """Meta class for `MonitoringConsolidatedClassesSerializer` serializer."""
        model = models.MonitoringConsolidated
        id_field = False
        fields = ('no_estagio',)


class MonitoringConsolidatedTableSerializer(serializers.ModelSerializer):
    """Serializer for table 'MonitoringConsolidatedClassesSerializer' data."""

    class Meta:
        """Meta class for `MonitoringConsolidatedTableSerializer` serializer."""
        model = models.MonitoringConsolidated
        id_field = False
        fields = (
            'id',
            'no_imagem',
            'dt_imagem',
            'no_estagio',
            'nu_orbita',
            'nu_ponto',
            'nu_latitude',
            'nu_longitude',
            'dt_t_zero',
            'dt_t_um',
            'co_funai',
            'nu_area_km2',
            'nu_area_ha',
            'co_cr',
            'ds_cr',
            'no_ti',
            'ti_nu_area_ha',
        )

class xptoSerializers(serializers.ModelSerializer):
    """Serializer for table 'MonitoringConsolidatedClassesSerializer' data."""
    class Meta:
        """Meta class for `MonitoringConsolidatedTableSerializer` serializer."""
        model = models.MonitoringConsolidatedStats
        fields = "__all__"


class ConsultaMonitoramentoTIAgrupadoAnoTISerializer(serializers.ModelSerializer):
    ano = serializers.IntegerField()
    cr_nu_area_ha = serializers.FloatField()
    dg_nu_area_ha = serializers.FloatField()
    dr_nu_area_ha = serializers.FloatField()
    ff_nu_area_ha = serializers.FloatField()
    total_nu_area_ha = serializers.FloatField()

    class Meta:
        model = models.MonitoringConsolidatedStats
        fields = [
            'ano',
            'co_funai',
            'no_ti',
            'ti_nu_area_ha',
            'cr_nu_area_ha',
            'dg_nu_area_ha',
            'dr_nu_area_ha',
            'ff_nu_area_ha',
            'total_nu_area_ha'
        ]


class ConsultaMonitoramentoTIAgrupadoSerializer(serializers.ModelSerializer):
    cr_nu_area_ha = serializers.FloatField()
    dg_nu_area_ha = serializers.FloatField()
    dr_nu_area_ha = serializers.FloatField()
    ff_nu_area_ha = serializers.FloatField()
    total_nu_area_ha = serializers.FloatField()

    class Meta:
        model = models.MonitoringConsolidatedStats
        fields = [
            'co_funai',
            'no_ti',
            'ti_nu_area_ha',
            'cr_nu_area_ha',
            'dg_nu_area_ha',
            'dr_nu_area_ha',
            'ff_nu_area_ha',
            'total_nu_area_ha'
        ]


class ConsultaMonitoramentoTIAgrupadoAnoSerializer(serializers.ModelSerializer):
    ano = serializers.IntegerField()
    cr_nu_area_ha = serializers.FloatField()
    dg_nu_area_ha = serializers.FloatField()
    dr_nu_area_ha = serializers.FloatField()
    ff_nu_area_ha = serializers.FloatField()
    total_nu_area_ha = serializers.FloatField()

    class Meta:
        model = models.MonitoringConsolidatedStats
        fields = [
            'ano',
            'cr_nu_area_ha',
            'dg_nu_area_ha',
            'dr_nu_area_ha',
            'ff_nu_area_ha',
            'total_nu_area_ha'
        ]


class ConsultaMonitoramentoTerraIndigenaSerializer(serializers.ModelSerializer):
    cr_nu_area_ha = serializers.FloatField()
    dg_nu_area_ha = serializers.FloatField()
    dr_nu_area_ha = serializers.FloatField()
    ff_nu_area_ha = serializers.FloatField()
    total_nu_area_ha = serializers.FloatField()

    class Meta:
        model = models.MonitoringConsolidatedStats
        fields = [
            'co_funai',
            'no_ti',
            'dt_t_um',
            'ti_nu_area_ha',
            'cr_nu_area_ha',
            'dg_nu_area_ha',
            'dr_nu_area_ha',
            'ff_nu_area_ha',
            'total_nu_area_ha'
        ]
