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
        data = {
            'co_cr': instance.co_cr,
            'ds_cr': instance.ds_cr
        }
        for cr in ["COORDENACAO REGIONAL DE ", "COORDENACAO REGIONAL DO ", "COORDENACAO REGIONAL ",]:
            data['ds_cr'] = data['ds_cr'].removeprefix(cr)

        data['ds_cr'] = data['ds_cr'].title()
        return data
