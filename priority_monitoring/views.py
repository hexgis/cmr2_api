from rest_framework import generics, filters
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend

from priority_monitoring.serializers import(
    PriorityConsolidatedSerializer,
    PriorityConsolidatedTbSerializer
)

from priority_monitoring.models import (
    PriorityConsolidated,
    PriorityConsolidatedTb
)

from priority_monitoring.filters import PriorityConsolidatedFilter


class PriorityConsolidatedView(generics.ListAPIView):
    """Returns consolidated data from PriorityConsolidated model data."""

    queryset = PriorityConsolidated.objects.all()
    serializer_class = PriorityConsolidatedSerializer
    filterset_class = PriorityConsolidatedFilter
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('no_cr', 'no_ti', 'ranking')
