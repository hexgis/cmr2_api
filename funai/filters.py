from django_filters import rest_framework

from funai import models


class NumberInFilter(
    rest_framework.BaseInFilter,
    rest_framework.NumberFilter
):
    """Base class used for creating IN lookup filters to filter numbers."""
    pass


class LimiteTerraIndigenaFilter(rest_framework.FilterSet):
    """LimiteTerraIndigenaFilter data.

    Filters:
        co_cr (int): regional coordination code.
    """
    co_cr = NumberInFilter(
        field_name='co_cr',
        lookup_expression='in',
        required=False
    )

    class Meta:
        """Metaclass to `funai.LimiteTerraIndigenaFilter`."""
        model = models.LimiteTerraIndigena
        fields = (
            'co_cr',
        )
