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


class GeoTerraIndigenaSerializer(GeoFeatureModelSerializer):
    ds_cr = serializers.SerializerMethodField()
    instrumentos_gestao = serializers.SerializerMethodField()

    def get_ds_cr(self, obj):
        return obj.co_cr.ds_cr

    def get_instrumentos_gestao(self, obj):
        if obj.possui_ig:
            instrumentos = models.ManagementInstrument.objects.filter(
                co_funai=obj.co_funai)
            serializer = InstrumentoGestaoSerializer(instrumentos, many=True)
            return serializer.data
        return None

    class Meta:
        model = models.LimiteTerraIndigena
        geo_field = 'geom'
        id_field = False
        fields = '__all__'


class TiPropertiesSerializer(serializers.ModelSerializer):
    """Serializador para extrair apenas as propriedades de LimiteTerraIndigena."""
    ds_cr = serializers.SerializerMethodField()
    instrumentos_gestao = serializers.SerializerMethodField()

    def get_ds_cr(self, obj):
        return obj.co_cr.ds_cr

    def get_instrumentos_gestao(self, obj):
        if obj.possui_ig:
            instrumentos = models.ManagementInstrument.objects.filter(
                co_funai=obj.co_funai)
            serializer = InstrumentoGestaoSerializer(instrumentos, many=True)
            return serializer.data
        return None

    class Meta:
        model = models.LimiteTerraIndigena
        fields = (
            'id', 'ds_cr', 'instrumentos_gestao', 'no_ti', 'co_funai', 'no_grupo_etnico',
            'ds_fase_ti', 'ds_modalidade', 'ds_reestudo_ti', 'no_municipio', 'sg_uf',
            'st_faixa_fronteira', 'dt_em_estudo', 'ds_portaria_em_estudo', 'dt_delimitada',
            'ds_despacho_delimitada', 'dt_declarada', 'ds_portaria_declarada', 'dt_homologada',
            'ds_decreto_homologada', 'dt_regularizada', 'ds_matricula_regularizada',
            'ds_doc_resumo_em_estudo', 'ds_doc_resumo_delimitada', 'ds_doc_resumo_declarada',
            'ds_doc_resumo_homologada', 'ds_doc_resumo_regularizada',
            'nu_area_ha', 'dt_cadastro', 'possui_ig', 'co_cr'
        )


class InstrumentoGestaoSerializer(serializers.ModelSerializer):
    """ Instrumento de Gestão data """

    class Meta:
        model = models.ManagementInstrument
        fields = '__all__'
