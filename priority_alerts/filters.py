from django_filters import rest_framework

from priority_alerts import models


class AlertsFilter(rest_framework.FilterSet):
    """Django filter `models.UrgentAlerts` data.

    Filter:
        * co_funai (int): filtering Indigenous Lands using Funai code.
    """
    co_funai = rest_framework.NumberFilter(
        field_name='co_funai',
        lookup_expr='exact'
    )

    class Meta:
        """Meta class for `AlertsFilter` filter."""
        model = models.UrgentAlerts
        fields = ('co_funai',)
