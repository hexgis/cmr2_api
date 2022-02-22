from django_filters import rest_framework

from funai import models


class LimiteTerraIndigenaFilter(rest_framework.FilterSet):
    """LimiteTerraIndigenaFilter data.

    Filters:
        co_cr (int): regional coordination code.
    """
    co_cr = rest_framework.NumberFilter(
        field_name='co_cr',
        required=False
    )

    class Meta:
        """Metaclass to `funai.LimiteTerraIndigenaFilter`."""
        model = models.LimiteTerraIndigena
        fields = (
            'co_cr',
        )
