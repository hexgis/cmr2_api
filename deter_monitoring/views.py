from django.db.models import Count, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis import filters as gis_filters

from rest_framework import (
    permissions,
    generics,
    response,
    status
)

from deter_monitoring import (
    models,
    serializers,
    filters
)

class AuthModelMixIn:
    """Default Authentication for `deter_monitoring` views."""

    permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAuthenticated,)


class DeterTIDetailView(AuthModelMixIn, generics.RetrieveAPIView):
    """Detail data for `deter_monitoring.models.DeterTI`.

    Filters:
        * pk (int): filtering request poligon identifier.
    """

    queryset = models.DeterTI.objects.all()
    serializer_class = serializers.DeterTIDetailSerializer
    lookup_field = 'pk'
    filter_backends = (DjangoFilterBackend,)


class DeterTIView(AuthModelMixIn, generics.ListAPIView):
    """Returns list data for `deter_monitoring.models.DeterTI`.
    
    Fielters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code
        * class_name (list_str): Classification classes. E.g.: ????
        * satellite (list_str): filtering Satellite using identify.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """

    queryset = models.DeterTI.objects.all()
    serializer_class = serializers.DeterTISerializer
    filterset_class = filters.DeterTIFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


class DeterTITableView(AuthModelMixIn, generics.ListAPIView):
    """Returns list end geom data for `deter_monitoring.models.DeterTI`.

    Fielters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code
        * class_name (list_str): Classification classes. E.g.: ????
        * satellite (list_str): filtering Satellite using identify.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """

    queryset = models.DeterTI.objects.all()
    serializer_class = serializers.DeterTITableSerializer
    filterset_class = filters.DeterTIFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        gis_filters.InBBoxFilter,
        DjangoFilterBackend,
    )
# alto volume, variedade velocidade
# &in_bbox=-69.27978515625001,-9.879569652774814,-64.00634765625001,-8.064668502396389&co_cr=30202001845
# &in_bbox=-78.60717773437501,-12.71536762877211,-57.51342773437501,-4.850154078505659
# data preapraiton
# Data Science: big Data , domain analysis, data acquisition, data transformation, data visualizations, class DeterTIMapStatsView(AuthModelMixIn, generics.ListAPIView):
# modelo de ML: formulação matemática que explica o relacionamento entre os dados

class DeterTIMapStatsView(AuthModelMixIn, generics.ListAPIView):
    """Retrieves `deter_monitoring.models.DeterTI` map stats data.

    Fielters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code
        * class_name (list_str): Classification classes. E.g.: ????
        * satellite (list_str): filtering Satellite using identify.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """

    queryset = models.DeterTI.objects.all()
    serializer_class = serializers.DeterTIMapStatsSerializer
    filterset_class = filters.DeterTIFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

    def get(self, request) -> response.Response:
        data = self.filter_queryset(self.queryset).aggregate(
            area_total_km=Count('areatotalkm'),
            total=Sum('id')
        )
        return response.Response(data, status=status.HTTP_200_OK)


class DeterTITableStatsView(AuthModelMixIn, generics.ListAPIView):
    """Return four data set acoording to the selected grouping in the request.

    Fielters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code
        * class_name (list_str): Classification classes. E.g.: ????
        * satellite (list_str): filtering Satellite using identify.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).

    Group by:
        grouping (str): define applied data grouping. . E.g.:

    Returns group by in request field grouping:

    """
    # queryset = models.DeterTI.objects.all()
    # serializer_class = serializers.DeterTITableStatsSerializer
    # filterset_class = filters.DeterTIFilter
    # bbox_filter_field = 'geom'
    # filter_backends = (
    #     DjangoFilterBackend,
    #     gis_filters.InBBoxFilter,
    # )
    pass