from django.db import models

from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from monitoring import models


class MonitoringConsolidatedSerializer(gis_serializers.GeoFeatureModelSerializer):

    class Meta:
        model = models.MonitoringConsolidated
        geo_field = 'geom'
        id_field = False
        fields = (
            'id',
            'tb_ciclo_monitoramento_id',
            'no_imagem',
            'dt_imagem',
            'no_estagio',
            'dt_cadastro',
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

    class Meta:
        model = models.MonitoringConsolidated
        id_field = False
        fields = (
            'id',
            'tb_ciclo_monitoramento_id',
            'no_imagem',
            'dt_imagem',
            'no_estagio',
            'dt_cadastro',
            'dt_t_um',
            'co_funai',
            'nu_area_km2',
            'nu_area_ha',
            'co_cr',
            'ds_cr',
            'no_ti',
            'ti_nu_area_ha',
        )


class MonitoringConsolidatedClassesSerializer(serializers.ModelSerializer):

    def to_representation(self, instance) -> str:
        return f'{instance.no_estagio}'

    class Meta:
        model = models.MonitoringConsolidated
        id_field = False
        fields = ('no_estagio',)


class MonitoringConsolidatedTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonitoringConsolidated
        id_field = False
        fields = (
            'id',
            'tb_ciclo_monitoramento_id',
            'no_imagem',
            'dt_imagem',
            'no_estagio',
            'dt_cadastro',
            'dt_t_um',
            'co_funai',
            'nu_area_km2',
            'nu_area_ha',
            'co_cr',
            'ds_cr',
            'no_ti',
            'ti_nu_area_ha',
        )
