#from django.db.models import fields
from django_filters import rest_framework

from priority_monitoring import models



class PriorityConsolidatedAbstractFilter (rest_framework.FilterSet):
    # Ainda necessário vincular as tabelas do APP funai CR e TI com o Priority_monitoring
    # no_cr = rest_framework.CharFilter(
    #     field_name='no_cr',
    # )

    # no_ti = rest_framework.CharFilter(
    #     field_name='no_ti',
    # )

    nome_estagio = rest_framework.CharFilter(
        field_name='no_estagio',
    )

    start_date = rest_framework.DateFilter(
        field_name='dt_t0',
        lookup_expr='gte',
        #required=True
    )

    end_date = rest_framework.DateFilter(
        field_name='dt_t1',
        lookup_expr='lte',
        #required=True
    )

    prioridade = rest_framework.CharFilter(
        field_name='prioridade',
    )


class PriorityConsolidatedFilter (PriorityConsolidatedAbstractFilter):
    class Meta:
        model = models.PriorityConsolidated
        fields = [
            #'no_cr',
            #'no_ti',
            'no_estagio',
            'start_date',
            'end_date',
            'prioridade'
        ]