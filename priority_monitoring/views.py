from django.db.models import Sum, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis import filters as gis_filters
from rest_framework import (
    generics, filters, response, permissions, status, exceptions
)

from priority_monitoring import(
    serializers,
    models,
    filters as priority_filters
)


class AuthModelMixIn:
    """Default Authentication for monitoring views."""
    permission_classes = (permissions.AllowAny,)


class PriorityConsolidatedView(AuthModelMixIn, generics.ListAPIView):
    """Returns list data for `priority_monitoring.PriorityConsolidated`.

    Filters:
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
        * co_cr (int): Regional Coordination code.
        * co_funai (list): Indigenous Lands code.
        * start_date (str): filter for start date.
        * end (str): filter for end date.
        * priority (str): priority data.
    """

    queryset = models.PriorityConsolidated.objects.all()
    serializer_class = serializers.PriorityConsolidatedSerializer
    filterset_class = priority_filters.PriorityConsolidatedFilter
    ordering_fields = ('prioridade', 'nome_estagio')
    bbox_filter_field = 'geom'
    filter_backends = (
        gis_filters.InBBoxFilter,
        DjangoFilterBackend,
        filters.OrderingFilter
    )


class PriorityConsolidatedDetailView(
    AuthModelMixIn,
    generics.RetrieveAPIView
):
    """Detail data for `priority_monitoring.PriorityConsolidated`."""  """

    Paramter:
        geometry (boolean): returns with or without geometry
    """

    queryset = models.PriorityConsolidated.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        """Get method to return serializer detail.

        Returns serializers with or without geometry:

        Returns:
            `serializers.PriorityConsolidatedDetailSerializer` or
            `serializers.PriorityConsolidatedDetailGeomSerializer`
        """

        geometry_necessary = self.request.query_params.get('geometry')

        if geometry_necessary == 'false' :
            return serializers.PriorityConsolidatedDetailSerializer
        elif geometry_necessary == 'true':
            return serializers.PriorityConsolidatedDetailGeomSerializer
        else:
            raise exceptions.NotFound(
                "Parameters 'geometry' must receive the values ​​of: 'true' " \
                "or 'false'.",
                None
            )


class PriorityConsolidatedStatsView(AuthModelMixIn, generics.ListAPIView):
    """Retrieves `priority_monitoring.PriorityConsolidated` stats data.

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
    filterset_class = priority_filters.PriorityConsolidatedFilter
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


class PrioritiesDistinctedListView(AuthModelMixIn, generics.ListAPIView):
    """Lists `priority` for `priority_monitoring.PriorityConsolidated`."""
    queryset = models.PriorityConsolidated.objects.order_by(
        'prioridade').distinct('prioridade')
    serializer_class = serializers.PrioritiesDistinctedListSerializer


class PriorityConsolidatedTableView(AuthModelMixIn, generics.ListAPIView):
    
    serializer_class = serializers.PriorityConsolidatedTableSerializer
    queryset = models.PriorityConsolidated.objects.all()
    filterset_class = priority_filters.PriorityConsolidatedFilter
    filter_backends = (DjangoFilterBackend,)    



