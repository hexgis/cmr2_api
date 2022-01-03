from rest_framework import generics, filters as filters_DRF
from django.db.models.query import QuerySet
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
    filter_backends = (DjangoFilterBackend, filters_DRF.OrderingFilter)
    ordering_fields = ('prioridade', 'nome_estagio')
