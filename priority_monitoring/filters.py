from django_filters import rest_framework

from priority_monitoring import models


class NumberInFilter(
    rest_framework.BaseInFilter,
    rest_framework.NumberFilter
):
    """Base class used for creating IN lookup filters to filter numbers."""
    pass


class CharInFilter(rest_framework.BaseInFilter, rest_framework.CharFilter):
    """Base class used for creating IN lookup filters to filter characters."""
    pass


class PriorityConsolidatedFilter(rest_framework.FilterSet):
    """PriorityConsolidatedFilter data.

    Filters:
        stage (str): stage name. E.g.: CR, DG, FF, DR
        start_date (str): filtering start date
        end_date (str): filteringend date
        priority (str): priority level
    """
    # Ainda necessário vincular as tabelas do APP
    # funai CR e TI com o Priority_monitoring
    co_cr = rest_framework.NumberFilter(
        field_name='co_cr',
    )

    co_funai = NumberInFilter(
        field_name='co_funai',
        lookup_expr='in',
    )

    stage = rest_framework.CharFilter(
        field_name='no_estagio',
    )

    start_date = rest_framework.DateFilter(
        field_name='dt_t1',
        lookup_expr='gte',
        required=True
    )

    end_date = rest_framework.DateFilter(
        field_name='dt_t1',
        lookup_expr='lte',
        required=True
    )

    priority = CharInFilter(
        field_name='prioridade',
        lookup_expr='in',
    )

    class Meta:
        """Meta class for `PriorityConsolidatedFilter` filter."""
        model = models.PriorityConsolidated
        fields = (
            'no_estagio',
            'start_date',
            'end_date',
            'priority',
            'co_cr',
            'co_funai'
        )
