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
        * id (int): filtering request poligon identifier.
    """

    queryset = models.DeterTI.objects.all()
    serializer_class = serializers.DeterTIDetailSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)

class DeterTIView(AuthModelMixIn, generics.ListAPIView):
    """Returns list data for `deter_monitoring.models.DeterTI`."""

    queryset = models.DeterTI.objects.all()
    serializer_class = serializers.DeterTISerializer
    filterset_class = filters.DeterTIFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

class DeterTableTIView(AuthModelMixIn, generics.ListAPIView):
    """Returns list end geom data for `deter_monitoring.models.DeterTI`."""

    queryset = models.DeterTI.objects.all()
    serializer_class = serializers.DeterTITableSerializer
    filterset_class = filters.DeterTIFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        gis_filters.InBBoxFilter,
        DjangoFilterBackend,
    )


class DeterTIMapStatsView(AuthModelMixIn, generics.ListAPIView):
    """Retrieves `deter_monitoring.models.DeterTI` map stats data."""

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
    """"""
    pass
    # queryset = models.DeterTI.objects.all()
    # serializer_class = serializers.DeterTITableStatsSerializer
    # filterset_class = filters.DeterTIFilter
    # bbox_filter_field = 'geom'
    # filter_backends = (
    #     DjangoFilterBackend,
    #     gis_filters.InBBoxFilter,
    # )