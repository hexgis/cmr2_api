from rest_framework.serializers import ModelSerializer

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
            'ds_cr'
        )
    def to_representation(self, instance):
        """Custom representation of the serialized data."""
        # Obtém o valor original do campo 'ds_cr'
        ds_cr = instance.ds_cr

        # Realize qualquer tratamento necessário no campo 'ds_cr' aqui
        # Por exemplo, você pode aplicar uma formatação específica ou filtrar os dados
        
        ds_cr = ds_cr.replace("COORDENACAO REGIONAL", "")
        # Retorna o valor tratado
        return ds_cr.strip()
