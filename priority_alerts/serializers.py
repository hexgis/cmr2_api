from rest_framework import serializers

from rest_framework_gis import serializers as gis_serializers

from priority_alerts import models


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
