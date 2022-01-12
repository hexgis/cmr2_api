from django.db import models
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from priority_monitoring import models


class PriorityConsolidatedSerializer(
    gis_serializers.GeoFeatureModelSerializer
):
    """Serializer for `models.PriorityConsolidated` data."""
    class Meta:
        model = models.PriorityConsolidated
        geo_field = 'geom'
        id_field = False
        fields = (
            'pk',
            'nu_area_km2',
            'prioridade',
        )


class PriorityConsolidatedDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed `models.PriorityConsolidated` data."""

    class Meta:
        model = models.PriorityConsolidated
        id_field = False
        fields = (
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
