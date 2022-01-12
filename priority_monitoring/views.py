from rest_framework import generics, filters
from rest_framework_gis import filters as gis_filters

from django_filters.rest_framework import DjangoFilterBackend

from priority_monitoring import(
    serializers,
    models,
    filters as filters_priority
)


class PriorityConsolidatedView(generics.ListAPIView):
    """Returns consolidated data from PriorityConsolidated model data."""

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


class PriorityConsolidatedDetailView(generics.RetrieveAPIView):
    """Returns consolidated data from PriorityConsolidated model data."""

    queryset = models.PriorityConsolidated.objects.all()
    serializer_class = serializers.PriorityConsolidatedDetailSerializer
    lookup_field = 'pk'
