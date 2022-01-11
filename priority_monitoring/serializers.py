from django.db import models
from rest_framework_gis import serializers as gis_serializers
from rest_framework import serializers

from priority_monitoring import models


class PriorityConsolidatedTempSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.PriorityConsolidatedTemp
        fields= '__all__'


class PriorityConsolidatedSerializer(gis_serializers.GeoFeatureModelSerializer):

    class Meta:
        model= models.PriorityConsolidated
        geo_field = 'geom'
        id_field = False
        fields= (
            'no_estagio',
            'no_image',
            'dt_image',
            'nu_orbita',
            'nu_ponto',
            'dt_t0',
            'dt_t1',
            'nu_area_km2',
            'nu_area_ha',
            'nu_latitude',
            'nu_longitude',
            'tempo',
            'contribuicao',
            'velocidade',
            'contiguidade',
            'ranking',
            'prioridade',
        )