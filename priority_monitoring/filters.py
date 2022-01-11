#from django.db.models import fields
from django_filters import rest_framework

from priority_monitoring import models


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
    # no_cr = rest_framework.CharFilter(
    #     field_name='no_cr',
    # )

    # no_ti = rest_framework.CharFilter(
    #     field_name='no_ti',
    # )

    stage = rest_framework.CharFilter(
        field_name='no_estagio',
    )

    start_date = rest_framework.DateFilter(
        field_name='dt_t1',
        lookup_expr='gte',
        # required=True
    )

    end_date = rest_framework.DateFilter(
        field_name='dt_t1',
        lookup_expr='lte',
        # required=True
    )

    priority = rest_framework.CharFilter(
        field_name='prioridade',
    )

    class Meta:
        model = models.PriorityConsolidated
        fields = (
            'no_estagio',
            'start_date',
            'end_date',
            'prioridade'
        )
