#from django.db.models import fields
import django_filters

from priority_monitoring import models



class PriorityConsolidatedAbstractFilter (django_filters.rest_framework.FilterSet):
    no_cr = django_filters.rest_framework.CharFilter(
        field_name='no_cr',
    )

    no_ti = django_filters.rest_framework.CharFilter(
        field_name='no_ti',
    )

    start_date = django_filters.rest_framework.DateFilter(
        field_name='dt_t_um',
        lookup_expr='gte',
        #required=True
    )

    end_date = django_filters.rest_framework.DateFilter(
        field_name='dt_t_um',
        lookup_expr='lte',
        #required=True
    )

    ranking = django_filters.rest_framework.CharFilter(
        field_name='ranking',
    )

class PriorityConsolidatedFilter (PriorityConsolidatedAbstractFilter):
    class Meta:
        model = models.PriorityConsolidated
        fields = [
            'no_cr',
            'no_ti',
            'start_date',
            'end_date',
            'ranking'
        ]