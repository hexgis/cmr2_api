from rest_framework import generics, response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, F, Func, Value
from permission.mixins import Auth, Public
from django.db.models.functions import Lower
from rest_framework.exceptions import NotFound, ValidationError
from django.conf import settings
import requests

from funai import (
    serializers,
    models,
    filters as filters_funai
)

from rest_framework.permissions import AllowAny


FIELD_TI_NAME = 'no_ti'
FIELD_CITY = 'no_municipio'
FIELD_CR_NAME = 'ds_cr'

SQL_UNACCENT = 'unaccent'


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
            Parameters:
                id (int): code for Indigenous Lands geodata.
    """
    serializer_class = serializers.GeoTerraIndigenaSerializer

    def get_queryset(self):
        queryset = models.LimiteTerraIndigena.objects.all()
        id = self.request.query_params.get('id', None)
        if id is None:
            raise ValidationError("O id é obrigatório.")

        queryset = models.LimiteTerraIndigena.objects.filter(id=id)
        return queryset


class TiByNameView(generics.ListAPIView):
    """
        View de apresentação de dados de Terra Indígena.
            Parameters:
                no_ti (string): name of Indigenous Lands.
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
        queryset = self.get_queryset().values(
            'id', 'no_ti', 'no_municipio', 'ds_cr', 'ds_fase_ti')
        data = list(queryset)
        return response.Response(data)


class TiByNameAllInfoView(Public, generics.ListAPIView):
    """
    API view to retrieve information about Indigenous Lands (TIs) based on a query parameter.
    Provides a list of TIs filtered and ordered by name.
    """

    serializer_class = serializers.TiPropertiesSerializer

    def get_queryset(self):
        """
        Retrieves the queryset for the Indigenous Lands (TIs).
        Filters the queryset based on the 'param' query parameter,
        ignoring accents and performing a case-insensitive match.

        Returns:
            QuerySet: A filtered and ordered queryset of `LimiteTerraIndigena` objects.
        """
        param = self.request.GET.get('param', None)
        queryset = models.LimiteTerraIndigena.objects.all()

        if param:
            search_value = param.strip().lower()
            unaccented_value = Func(Value(search_value), function=SQL_UNACCENT)

            queryset = queryset.annotate(
                no_ti_unaccent=Func(
                    Lower(FIELD_TI_NAME),
                    function=SQL_UNACCENT
                ),
                no_municipio_unaccent=Func(
                    Lower(FIELD_CITY),
                    function=SQL_UNACCENT
                ),
                co_cr__ds_cr_unaccent=Func(
                    Lower(FIELD_CR_NAME),
                    function=SQL_UNACCENT),

            ).filter(
                Q(no_ti_unaccent__icontains=unaccented_value) |
                Q(no_municipio_unaccent__icontains=unaccented_value) |
                Q(co_cr__ds_cr_unaccent__icontains=unaccented_value)

            )

        return queryset.order_by(FIELD_TI_NAME)

    def list(self, request, *args, **kwargs):
        """
        Overrides the default list method to serialize and return the queryset data.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A JSON response containing serialized data of the filtered queryset.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class IndegenousVillageByNameView(generics.ListAPIView):

    def get_indegenous_village(self):
        # Geoserver parameters
        geoserver_url = settings.GEOSERVER_URL
        params = {
            'service': 'WFS',
            'version': '1.0.0',
            'request': 'GetFeature',
            'typeName': f'CMR-PUBLICO:{settings.GEO_SEARCH_VILLAGE}',
            'outputFormat': 'application/json',
            'authkey': f'{settings.SECRET_KEY}'
        }
        param = self.request.GET.get('param', None)
        if param:
            params['cql_filter'] = f"no_aldeia LIKE '%{param}%'"

        response = requests.get(geoserver_url, params=params, verify=False)

        if response.status_code == 200:
            data = response.json()
            features = data.get('features', [])
            filtered_data = [
                {
                    'id': feature.get('id', ''),
                    'no_aldeia': feature['properties'].get('no_aldeia', ''),
                    'no_municipio': feature['properties'].get('no_municipio', ''),
                    'ds_cr': feature['properties'].get('ds_cr', ''),
                    'ds_fase_ti': "",
                }
                for feature in features
            ]
            return filtered_data
        else:
            return []

    def list(self, request, *args, **kwargs):
        # Overriding the list method to use the response from get_queryset directly
        queryset = self.get_indegenous_village()
        return response.Response(queryset)


class TiInStudyByName(generics.ListAPIView):

    def get_indegenous_village(self):
        # Geoserver parameters
        geoserver_url = settings.GEOSERVER_URL
        params = {
            'service': 'WFS',
            'version': '1.0.0',
            'request': 'GetFeature',
            'typeName': f'CMR-PUBLICO:{settings.GEO_SEARCH_STUDY_TI}',
            'outputFormat': 'application/json',
            'authkey': f'{settings.SECRET_KEY}'
        }
        param = self.request.GET.get('param', None)
        if param:
            params['cql_filter'] = f"no_ti LIKE '%{param}%'"

        response = requests.get(geoserver_url, params=params, verify=False)

        if response.status_code == 200:
            data = response.json()
            features = data.get('features', [])
            filtered_data = [
                {
                    'id': feature.get('id', ''),
                    'no_ti': feature['properties'].get('no_ti', ''),
                    'no_municipio': feature['properties'].get('no_municipio', ''),
                    'ds_cr': feature['properties'].get('ds_cr', ''),
                    'ds_fase_ti': "",
                }
                for feature in features
            ]
            return filtered_data
        else:
            return []

    def list(self, request, *args, **kwargs):
        # Overriding the list method to use the response from get_queryset directly
        queryset = self.get_indegenous_village()
        return response.Response(queryset)
