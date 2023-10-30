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
