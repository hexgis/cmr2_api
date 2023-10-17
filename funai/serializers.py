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
    # def to_representation(self, instance):
    #     """Custom representation of the serialized data."""
    #     ds_cr = instance.ds_cr
    #     ds_cr = ds_cr.replace("COORDENACAO REGIONAL", "")
    #     return ds_cr.strip()
