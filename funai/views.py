from rest_framework import generics, response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, F, Func, Value

from django.db.models.functions import Lower
from rest_framework import generics
from rest_framework.exceptions import NotFound, ValidationError


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

class TiByNameView(generics.ListAPIView):
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

class BuscaInstrumentoGestaoView(generics.ListAPIView):
    """
        View de apresentação dos dados de isntrumento de gestão com base no co_funai fornecido 
    """
    serializer_class = serializers.GeoTerraIndigenaSerializer

    def get_queryset(self):
        queryset = models.LimiteTerraIndigena.objects.all()
        co_funai = self.request.query_params.get('co_funai', None)
        if co_funai is None:
            raise ValidationError("O código funai é obrigatório.")
        
        queryset = models.LimiteTerraIndigena.objects.filter(co_funai=co_funai)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            raise NotFound("Nenhum registro encontrado para o código fornecido.")
        
        instrumentos_gestao = []
        for obj in queryset:
            if obj.possui_ig:
                instrumentos = models.InstrumentoGestaoFunai.objects.filter(co_funai=obj.co_funai)
                serializer = serializers.InstrumentoGestaoSerializer(instrumentos, many=True)
                instrumentos_gestao.append(serializer.data)
            else:
                instrumentos_gestao.append(None)
        
        return response.Response(instrumentos_gestao)
