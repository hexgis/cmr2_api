from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis import filters as gis_filters

from rest_framework import (
    permissions,
    generics,
    response,
)

from deter_monitoring import (
    models,
    serializers
)

class AuthModelMixIn:
    """Default Authentication for `deter_monitoring` views."""

    permission_classes = (permissions.AllowAny,)


class DeterDetailView(AuthModelMixIn, generics.RetrieveAPIView):
    """Detail data for `deter_monitoring.models.DeterTable`.

    Filters:
        * id (int): filtering request poligon identifier.
    """

    queryset = models.DeterTable.objects.all()
    serializer_class = serializers.DeterDetailSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)


class DeterView(AuthModelMixIn, generics.ListAPIView):
    """Returns list end geom data for `deter_monitoring.models.DeterTable`."""

    queryset = models.DeterTable.objects.all()
    serializer_class = serializers.DeterSerializer
    bbox_filter_field = 'geom'
    filter_backends = (
        gis_filters.InBBoxFilter,
        DjangoFilterBackend,
    )


class DeterMapStatsView(AuthModelMixIn, generics.ListAPIView):
    """Retrieves `deter_monitoring.models.DeterTable` map stats data."""
    pass
    # queryset = models.DeterTable.objects.all()
    # serializer_class = serializers.DeterMapStatsSerializer


class DeterTableView(AuthModelMixIn, generics.ListAPIView):
    """Returns list data for `deter_monitoring.models.DeterTable`."""

    queryset = models.DeterTable.objects.all()
    serializer_class = serializers.DeterTableSerializer
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


class DeterTableStatsView(AuthModelMixIn, generics.ListAPIView):
    """"""
    pass
    # queryset = models.DeterTable.objects.all()
    # serializer_class = serializers.DeterTableStatsSerializer
    # filter_backends = (
    #     DjangoFilterBackend,
    #     gis_filters.InBBoxFilter,
    # )