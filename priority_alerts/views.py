from priority_alerts import (
    serializers,
    models,
    filters as alerts_filters
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis import filters as gis_filters
from rest_framework import (
    permissions,
    generics
)


class AuthModelMixIn:
    """Default Authentication for priority_alerts views."""
    permission_class = (permissions.AllowAny,)


class AlertsView(generics.ListAPIView):
    """Returns the list of `models.UrgentAlerts` spatial data.

    Filters:
        * co_cr (list): filtering Regional Coordiantion using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * start_date (str): filtering start date.
        * end_date (str): filteringend end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """
    queryset = models.UrgentAlerts.objects.all()
    serializer_class = serializers.AlertsSerializers
    filterset_class = alerts_filters.AlertsFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


class AlertsTableView(generics.ListAPIView):
    """Returns list data without geometry from 'models.UrgentAlerts' data.

    Filters:
        * co_cr (list): filtering Regional Coordiantion using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * start_date (str): filtering start date.
        * end_date (str): filteringend end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """
    queryset = models.UrgentAlerts.objects.all()
    serializer_class = serializers.AlertsTableSerializers
    filterset_class = alerts_filters.AlertsFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


class AlertsDetailView(generics.RetrieveAPIView):
    """Returns detailed data for a queried element of `models.UrgentAlerts` 
    data.

    Filters:
        * id (int): filtering request poligon identifier.
    """
    queryset = models.UrgentAlerts.objects.all()
    serializer_class = serializers.AlertsTableSerializers
    lookup_field = 'id'


class AlertsStatsView(generics.ListAPIView):
    """Retrives `models.UrgentAlerts` stats data.

    Filters:
        * co_cr (list): filtering Regional Coordiantion using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * start_date (str): filtering start date.
        * end_date (str): filteringend end date.
    """
    pass


class AlertsClassesView(generics.ListAPIView):
    """Flag list classification stages adopted in mapping the monitoring of 
    indigenous land `models.UrgentAlerts` existing in the applied filters.

    Filters:
        * co_cr (list): filtering Regional Coordiantion using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * start_date (str): filtering start date.
        * end_date (str): filteringend end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """
    queryset = models.UrgentAlerts.objects.distinct('nu_referencia')
    serializer_class = serializers.AlertsClassesSerializers
    filterset_class = alerts_filters.AlertsFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )
