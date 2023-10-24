from rest_framework import generics, response
from django_filters.rest_framework import DjangoFilterBackend

from funai import(
    serializers,
    models,
    filters as filters_funai
)


class CoordenacaoRegionalView(generics.ListAPIView):
    """CoordenacaoRegionalView view for Regional Coordination data."""

    queryset = models.CoordenacaoRegional.objects.all()
    serializer_class = serializers.CoordenacaoRegionalSerializer

    def list(self, request):
        serializer= serializers.CoordenacaoRegionalSerializer(
            models.CoordenacaoRegional.objects.all(), many=True)
        serializer_data= sorted(serializer.data, key=lambda k: (k['no_regiao'],k['ds_cr']))

        return response.Response(serializer_data)


class LimiteTerraIndigenaView(generics.ListAPIView):
    """LimiteTerraIndigenaView view for Indigenous Lands data.

    Filters:
        co_cr (int): code for Regional Coordination.
    """

    queryset = models.LimiteTerraIndigena.objects.all()
    serializer_class = serializers.LimiteTerraIndigenaSerializer
    filterset_class = filters_funai.LimiteTerraIndigenaFilter
    filter_backends = (DjangoFilterBackend,)
