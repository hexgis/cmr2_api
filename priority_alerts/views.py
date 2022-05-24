from rest_framework import (
    permissions, generics
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis import filters as gis_filters
from priority_alerts import (
    serializers,
    models,
    filters as alerts_filters
)


class AuthModelMixIn:
    permission_class = (permissions.AllowAny,)


class AlertsView(generics.ListAPIView):
    queryset = models
    serializer_class = serializers.AlertsSerializers
    filterset_class = alerts_filters.AlertsFilter
    bbox_filter_field = 'geom'
    filter_backend = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,)


class AlertsTableView(generics.ListAPIView):
    queryset = models.UrgentAlerts
    serializers_class = serializers.AlertsTableSerializers
    filterset_class = alerts_filters.AlertsFilter
    bbox_filter_field = 'geom'
    filter_backend = (DjangoFilterBackend,)


class AlertsDetailView(generics.RetrieveAPIView):
    queryset = models.UrgentAlerts
    serializers_class = serializers.AlertsDetailSerializers
    filterset_class = alerts_filters.AlertsFilter
    bbox_filter_field = 'geom'
    filter_backend = (DjangoFilterBackend,)


class AlertsStatsView(generics.ListAPIView):
    queryset = models.UrgentAlerts
    serializers_class = serializers.AlertsStatsSerializers
    filterset_class = alerts_filters.AlertsFilter
    bbox_filter_field = 'geom'
    filter_backend = (DjangoFilterBackend,)


class AlertsClassesView(generics.ListAPIView):
    queryset = models.UrgentAlerts
    serializers_class = serializers.AlertsClassesSerializers
    filterset_class = alerts_filters.AlertsFilter
    bbox_filter_field = 'geom'
    filter_backend = (DjangoFilterBackend,)
