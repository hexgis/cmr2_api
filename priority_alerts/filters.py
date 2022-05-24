from django_filters import rest_framework

from priority_alerts import models


class AlertsFilter(rest_framework.FilterSet):
    co_funai = rest_framework.NumberFilter(
        field_name='co_funai',
        lookup_expr='exact'
    )

    class Meta:
        model = models.UrgentAlerts
        fields = ('co_funai',)
