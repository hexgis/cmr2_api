from django_filters import rest_framework

from deter_monitoring import models


# class NumberInFilter(
#     rest_framework.BaseInFilter,
#     rest_framework.NumberFilter
# ):
#     """Base class used for creating IN lookup filters to filter numbers."""
#     pass


class CharInFilter(
    rest_framework.BaseInFilter,
    rest_framework.CharFilter
):
    """Base class used for creating IN lookup filters to filter characters."""
    pass


class DeterTIFilter(rest_framework.FilterSet):
    """DeterTIFilter data.

    Fielters:
        * class_name (list_str): Classification classes. E.g.: ????
        * satellite (list_str): filtering Satellite using identify.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
    """

    class_name = CharInFilter(
        field_name='classname',
        lookup_expr='in',
    )
    satellite = CharInFilter(
        field_name='satellite',
        lookup_expr='in',
    )
    start_date = rest_framework.DateFilter(
        field_name='view_date',
        lookup_expr='gte',
    )
    end_date = rest_framework.DateFilter(
        field_name='view_date',
        lookup_expr='lte',
    )

    class Meta:
        """Meta class for `DeterTIFilter` filter."""
        model = models.DeterTI
        fields = (
            'class_name',
            'satellite',
            'start_date',
            'end_date'
        )
