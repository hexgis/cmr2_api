from django_filters import rest_framework

from monitoring import models


class NumberInFilter(
    rest_framework.BaseInFilter,
    rest_framework.NumberFilter
):
    pass


class MonitoringConsolidatedFilter(rest_framework.FilterSet):

    co_cr = NumberInFilter(
        field_name='co_cr',
        lookup_expr='in'
    )

    co_funai = NumberInFilter(
        field_name='co_funai',
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
        model = models.MonitoringConsolidated
        fields = (
            'dt_t_um',
            'co_cr',
            'co_funai',
        )
