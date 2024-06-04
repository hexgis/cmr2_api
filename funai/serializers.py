from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers

from funai import models


class LimiteTerraIndigenaSerializer(ModelSerializer):
    """LimiteTerraIndigenaSerializer data."""

    class Meta:
        """Metaclass to `funai.LimiteTerraIndigenaSerializer`."""
        model = models.LimiteTerraIndigena
        fields = (
            'co_funai',
            'no_ti'
        )


class CoordenacaoRegionalSerializer(ModelSerializer):
    """CoordenacaoRegionalSerializer model data."""

    class Meta:
        """Metaclass to `funai.CoordenacaoRegionalSerializer`."""
        model = models.CoordenacaoRegional
        fields = (
            'co_cr',
            'ds_cr',
            'no_regiao'
        )

    def to_representation(self, instance):
        """Method to return in `CoordenacaoRegionalSerializer` the data processed from
        the names of the Regional Coordinations. 

        Returns:
            collections.OrderedDict list: data with the "ds_cr" field treated
        """
        data = super().to_representation(instance)
        data['ds_cr'] = data['ds_cr'].title()
        for cr in [
            "Coordenacao Regional De ",
            "Coordenacao Regional Do ",
            "Coordenacao Regional ",
        ]:
            data['ds_cr'] = data['ds_cr'].removeprefix(cr)
        return data

class InstrumentoGestaoSerializer(ModelSerializer):
    """ Instrumento de Gestão data """

    class Meta: 
        model = models.InstrumentoGestaoFunai
        exclude = ['id', 'co_funai', 'no_ti', 'sg_uf']

class GeoTerraIndigenaSerializer(GeoFeatureModelSerializer):
    ds_cr = serializers.SerializerMethodField()
    instrumentos_gestao = serializers.SerializerMethodField()

    def get_ds_cr(self, obj):
        return obj.co_cr.ds_cr

    def get_instrumentos_gestao(self, obj):
        if obj.possui_ig:
            instrumentos = models.InstrumentoGestaoFunai.objects.filter(co_funai=obj.co_funai)
            serializer = InstrumentoGestaoSerializer(instrumentos, many=True)
            return serializer.data
        return None

    class Meta:
        model = models.LimiteTerraIndigena
        geo_field = 'geom'
        id_field = False
        fields = '__all__'

