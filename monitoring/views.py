from django.db.models import Sum, Count

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis import filters as gis_filters
from rest_framework import (
    generics, response, permissions, status
)

from monitoring import (
    serializers,
    models,
    filters as monitoring_filters
)


class AuthModelMixIn:

    permission_classes = (permissions.AllowAny,)


class MonitoringConsolidatedView(generics.ListAPIView, AuthModelMixIn):

    queryset = models.MonitoringConsolidated.objects.all()
    serializer_class = serializers.MonitoringConsolidatedSerializer
    filterset_class = monitoring_filters.MonitoringConsolidatedFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        gis_filters.InBBoxFilter,
        DjangoFilterBackend
    )


class MonitoringConsolidatedDetailView(generics.RetrieveAPIView, AuthModelMixIn):

    queryset = models.MonitoringConsolidated.objects.all()
    serializer_class = serializers.MonitoringConsolidatedDetailSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)


class MonitoringConsolidatedStatsView(generics.ListAPIView, AuthModelMixIn):

    queryset = models.MonitoringConsolidated.objects.all()
    serializer_class = serializers.MonitoringConsolidatedSerializer
    filterset_class = monitoring_filters.MonitoringConsolidatedFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

    def get(self, request):
        data = self.filter_queryset(self.queryset).aggregate(
            area_ha=Sum('nu_area_ha'),
            area_km=Sum('nu_area_km2'),
            total=Count('id')
        )

        return response.Response(data, status=status.HTTP_200_OK)


class MonitoringConsolidatedClassesView(generics.ListAPIView, AuthModelMixIn):

    queryset = models.MonitoringConsolidated.objects.order_by(
        'no_estagio').distinct('no_estagio'
                               )
    serializer_class = serializers.MonitoringConsolidatedClassesSerializer


class MonitoringConsolidatedTableView(generics.ListAPIView, AuthModelMixIn):

    queryset = models.MonitoringConsolidated.objects.all()
    serializer_class = serializers.MonitoringConsolidatedTableSerializer
    filterset_class = monitoring_filters.MonitoringConsolidatedFilter
    filter_backends = (DjangoFilterBackend,)
