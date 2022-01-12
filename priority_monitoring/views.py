from rest_framework import (
    generics, filters, response, permissions, status
)

from rest_framework_gis import filters as gis_filters

from django.db.models import Sum, Count
from django_filters.rest_framework import DjangoFilterBackend

from priority_monitoring import(
    serializers,
    models,
    filters as filters_priority
)


class AuthModelMixIn:
    """Default Authentication for monitoring views."""
    pass
    permission_classes = (permissions.AllowAny,)


class PriorityConsolidatedView(AuthModelMixIn, generics.ListAPIView):
    """Returns consolidated data for `models.PriorityConsolidated` model data.

    Filters:
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
        * co_cr (int): Regional Coordination code.
        * co_funai (int): Indigenous Lands code.
        * start_date (str): filter for start date.
        * end (str): filter for end date.
        * priority (str): priority data.
    """

    queryset = models.PriorityConsolidated.objects.all()
    serializer_class = serializers.PriorityConsolidatedSerializer
    filterset_class = filters_priority.PriorityConsolidatedFilter
    ordering_fields = ('prioridade', 'nome_estagio')
    bbox_filter_field = 'geom'
    filter_backends = (
        gis_filters.InBBoxFilter,
        DjangoFilterBackend,
        filters.OrderingFilter
    )


class PriorityConsolidatedDetailView(AuthModelMixIn, generics.RetrieveAPIView):
    """Returns consolidated data from PriorityConsolidated model data."""

    queryset = models.PriorityConsolidated.objects.all()
    serializer_class = serializers.PriorityConsolidatedDetailSerializer
    lookup_field = 'pk'


class PriorityConsolidatedStatsView(AuthModelMixIn, generics.ListAPIView):
    """API for listing `models.PriorityConsolidated` total data.

    Filters:
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
        * co_cr (int): Regional Coordination code.
        * co_funai (int): Indigenous Lands code.
        * start_date (str): filter for start date.
        * end (str): filter for end date.
        * priority (str): priority data.
    """
    queryset = models.PriorityConsolidated.objects.all()
    serializer_class = serializers.PriorityConsolidatedSerializer
    filterset_class = filters_priority.PriorityConsolidatedFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        gis_filters.InBBoxFilter,
        DjangoFilterBackend,
    )

    def get(self, request):
        """Get method to return stats for Monitoring.

        Returns sums for area_ha, area_km and registry.

        Returns:
            rest_framework.Response.response: api response data.
        """
        data = self.filter_queryset(self.queryset).aggregate(
            area_ha=Sum('nu_area_ha'),
            area_km=Sum('nu_area_km2'),
            total=Count('id')
        )
        return response.Response(data, status=status.HTTP_200_OK)
