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


class DeterTIDetailView(AuthModelMixIn, generics.RetrieveAPIView):
    """Detail data for `deter_monitoring.models.DeterTI`.

    Filters:
        * pk (int): filtering request poligon identifier.
    """

    queryset = models.DeterTI.objects.all()
    serializer_class = serializers.DeterTIDetailSerializer
    lookup_field = 'pk'
    filter_backends = (DjangoFilterBackend,)


class DeterTIClassView(AuthModelMixIn, generics.ListAPIView):
    """This class for `deter_monitoring.models.DeterTI` inheritance view.

    Filters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * stage (list_str): Classification classes. E.g.:
            "CICATRIZ_DE_QUEIMADA"; "DESMATAMENTO_VEG"; "CS_DESORDENADO";
            "DESMATAMENTO_CR"; "CS_GEOMETRICO"; "DEGRADACAO"; "MINERACAO"
        * satellite (list_str): filtering Satellite using identify.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """

    queryset = models.DeterTI.objects.all()
    filterset_class = filters.DeterTIFilters
    bbox_filter_field = 'geom'
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


class DeterTIView(DeterTIClassView):
    """Returns list data for `deter_monitoring.models.DeterTI`.

    Filters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code
        * stage (list_str): Classification classes. E.g.:
            "CICATRIZ_DE_QUEIMADA"; "DESMATAMENTO_VEG"; "CS_DESORDENADO";
            "DESMATAMENTO_CR"; "CS_GEOMETRICO"; "DEGRADACAO"; "MINERACAO"
        * satellite (list_str): filtering Satellite using identify.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """

    serializer_class = serializers.DeterTISerializer


class DeterTITableView(DeterTIClassView):
    """Returns list end geom data for `deter_monitoring.models.DeterTI`.

    Filters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code
        * stage (list_str): Classification classes. E.g.:
            "CICATRIZ_DE_QUEIMADA"; "DESMATAMENTO_VEG"; "CS_DESORDENADO";
            "DESMATAMENTO_CR"; "CS_GEOMETRICO"; "DEGRADACAO"; "MINERACAO"
        * satellite (list_str): filtering Satellite using identify.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """

    serializer_class = serializers.DeterTITableSerializer


class DeterTIMapStatsView(DeterTIClassView):
    """Retrieves `deter_monitoring.models.DeterTI` map stats data.

    Filters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code
        * stage (list_str): Classification classes. E.g.:
            "CICATRIZ_DE_QUEIMADA"; "DESMATAMENTO_VEG"; "CS_DESORDENADO";
            "DESMATAMENTO_CR"; "CS_GEOMETRICO"; "DEGRADACAO"; "MINERACAO"
        * satellite (list_str): filtering Satellite using identify.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """

    serializer_class = serializers.DeterTIMapStatsSerializer

    def get(self, request) -> response.Response:
        """Get method to return stats maps for Deter.

        Returns sums for area_km and count poligons.

        Args:
            request (Requests.request): Request data.

        Returns:
            response.Response: 
                django rest_framework.Response.response api response data.
        """
        data = self.filter_queryset(self.queryset).aggregate(
            area_km=Sum('areatotalkm'),
            total=Count('id')
        )
        return response.Response(data, status=status.HTTP_200_OK)
