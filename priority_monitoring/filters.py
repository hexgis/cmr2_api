from django_filters import rest_framework

from priority_monitoring import models


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


class PriorityConsolidatedFilter(rest_framework.FilterSet):
    """PriorityConsolidatedFilter data.

    Filters:
        * co_cr (list_int): Regional Coordination code.
        * co_funai (list_str): Indigenous Lands code.
        * stage (list_str): Classification stage. E.g.: CR, DG, FF, DR
        * start_date (str): Filter for start date.
        * end_date (str): Filter for end date.
        * priority (str): Priority level.
    """
    # Ainda necessário vincular as tabelas do APP
    # funai CR e TI com o Priority_monitoring
    co_cr = NumberInFilter(
        field_name='co_cr',
        lookup_expr='in',
    )

    co_funai = NumberInFilter(
        field_name='co_funai',
        lookup_expr='in',
    )

    stage = CharInFilter(
        field_name='no_estagio',
        lookup_expr='in',
    )

    start_date = rest_framework.DateFilter(
        field_name='dt_t_um',
        lookup_expr='gte',
        required=True
    )

    end_date = rest_framework.DateFilter(
        field_name='dt_t_um',
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
