from rest_framework import generics, response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, F, Func, Value

from django.db.models.functions import Lower
from rest_framework import generics


from funai import (
    serializers,
    models,
    filters as filters_funai
)

class Unaccent(Func):
    function = 'unaccent'
    template = '%(function)s(%(expressions)s)'


class CoordenacaoRegionalView(generics.ListAPIView):
    """CoordenacaoRegionalView view for Regional Coordination data."""

    queryset = models.CoordenacaoRegional.objects.all()
    serializer_class = serializers.CoordenacaoRegionalSerializer

    def list(self, request):
        """Instantiating the serializer `funai.CoordenacaoRegionalSerializer`, list a
        queryset overriding the LIST method to sort the response in ascending 
        alphabetical order by 'no_regiao' and 'ds_cr'.

        Returns:
            rest_framework.response.Response: Return the serialized data sorted
        """
        serializer = serializers.CoordenacaoRegionalSerializer(
            models.CoordenacaoRegional.objects.all(), many=True)
        serializer_data = sorted(serializer.data, key=lambda k: (
            # k['no_regiao'],
            k['ds_cr']
        ))

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


class BuscaGeoTIListView(generics.ListAPIView):
    """
    View de apresentação de dados de Terra Indígena em formato geojson para a aplicação
    """
    serializer_class = serializers.GeoTerraIndigenaSerializer
    queryset = models.LimiteTerraIndigena.objects.all()


class TiByName(generics.ListAPIView):
    """
        View de apresentação de dados de Terra Indígena.
    """

    serializer_class = serializers.GeoTerraIndigenaSerializer

    def get_queryset(self):
        param = self.request.GET.get('param', None)
        queryset = models.LimiteTerraIndigena.objects.all()

        if param:
            param = param.lower()
            unaccented_param = Func(Value(param), function='unaccent')
            
            queryset = queryset.annotate(
                unaccented_no_ti=Unaccent(Lower('no_ti'))
            ).filter(
                Q(unaccented_no_ti__icontains=unaccented_param)
            )
        queryset = queryset.order_by('no_ti')

        return queryset
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().values('id', 'no_ti', 'no_municipio', 'ds_cr')
        data = list(queryset)
        return response.Response(data)
    