from django_filters import rest_framework

from monitoring import models


class NumberInFilter(
    rest_framework.BaseInFilter,
    rest_framework.NumberFilter
):
    """Base class used for creating IN lookup filters to filter numbers."""
    pass


class CharInFilter(
    rest_framework.BaseInFilter,
    rest_framework.CharFilter
):
    """Base class used for creating IN lookup filters to filter characters."""
    pass


class MonitoringConsolidatedFilter(rest_framework.FilterSet):
    """MonitoringConsolidatedFilter data.

    Filters:
        co_cr (list): filtering Regional Coordenation using code.
        co_funai (list): filtering Indigenou Lands using Funai code
        stage (list): stage name. E.g.: CR, DG, FF, DR
        start_date (str): filtering start date
        end_date (str): filtering end date
    """
    co_cr = NumberInFilter(
        field_name='co_cr',
        lookup_expr='in'
    )

    co_funai = NumberInFilter(
        field_name='co_funai',
        lookup_expr='in'
    )

    stage = CharInFilter(
        field_name='no_estagio',
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
        """Meta class for `MonitoringConsolidatedFilter` filter."""
        model = models.MonitoringConsolidated
        fields = (
            'co_cr',
            'co_funai',
            'stage',
            'start_date',
            'end_date',
        )
