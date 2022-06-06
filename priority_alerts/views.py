from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_gis import filters as gis_filters

from rest_framework import (
    permissions,
    generics,
    response,
    status
)

from django.db.models import (
    Count, 
    Sum
)

from priority_alerts import (
    serializers,
    models,
    filters as alerts_filters
)


class AuthModelMixIn:
    """Default Authentication for priority_alerts views."""
    permission_class = (permissions.AllowAny,)


class AlertsView(generics.ListAPIView):
    """Returns the list of `models.UrgentAlerts` spatial data.

    Filters:
        * co_cr (list): filtering Regional Coordiantion using code.
        * co_funai (list): filtering Indigenous Lands using Funai code.
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
        * co_funai (list): filtering Indigenous Lands using Funai code.
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
    """Returns detailed of queried element from `models.UrgentAlerts` data.

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

    def get (self, request):
        """Get method to return stats for priority_alerts.

        Returns sums for area_ha and registry.

        Args:
            request (Requests.request): Request data.

        Returns:
            response.Response: django rest_framework.Response.response api
            response data.
        """
        data = self.filter_queryset(self.queryset).aggregate(
            area_ha=Sum('nu_area_ha'),
            total=Count('id')
        )

        return response.Response(data, status=status.HTTP_200_OK)


class AlertsClassesView(generics.ListAPIView):
    """Flag list classification stages adopted in mapping the monitoring of 
    indigenous land `models.UrgentAlerts` existing in the applied filters.

    Filters:
        * co_cr (list): filtering Regional Coordiantion using code.
        * co_funai (list): filtering Indigenous Lands using Funai code.
        * start_date (str): filtering start date.
        * end_date (str): filteringend end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """
    queryset = models.UrgentAlerts.objects.distinct('no_estagio')
    serializer_class = serializers.AlertsClassesSerializers
    filterset_class = alerts_filters.AlertsFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )
