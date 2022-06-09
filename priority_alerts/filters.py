from django_filters import rest_framework

from priority_alerts import models

class NumberInFilter(
    rest_framework.BaseInFilter,
    rest_framework.NumberFilter
):
    """Base class used for creating IN lookup filters to filter numbers."""
    pass

class AlertsFilter(rest_framework.FilterSet):
    """Django filter `models.UrgentAlerts` data.

    Filter:
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * start_date (str): filtering start date.
        * end_date (str): filteringend ende date.
    """
    co_funai = NumberInFilter(
        field_name='co_funai',
        lookup_expr='in'
    )

    co_cr = NumberInFilter(
        field_name='co_cr',
        lookup_expr='in'
    )

    start_date = rest_framework.DateFilter(
        field_name='dt_t_um',
        lookup_expr='gte',
        required=False
    )

    end_date = rest_framework.DateFilter(
        field_name='dt_t_um',
        lookup_expr='lte',
        required=False
    )

    class Meta:
        """Meta class for `AlertsFilter` filter."""
        model = models.UrgentAlerts
        fields = (
            'co_funai',
            'co_cr',
            'start_date',
            'end_date',
        )
