from django_filters import rest_framework

from land_use import models


class NumberInFilter(
    rest_framework.NumberFilter,
    rest_framework.BaseInFilter
):
    """Base class used for creating IN lookup filters to filter numbers."""
    pass


class LandUseClassesFilter(rest_framework.FilterSet):
    """Django filter `models.LandUseClasses` data.

    Filters:
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * map_year (list): filtering years mapped in land use mapping.
    """
    co_cr = NumberInFilter(
        field_name='co_cr',
        lookup_expr='in'
    )

    co_funai = NumberInFilter(
        field_name='co_funai',
        lookup_expr='in'
    )

    map_year = NumberInFilter(
        field_name='nu_ano',
        lookup_expr='in'
    )

    class Meta:
        """Meta class for 'LandUseClassesFilter' filter."""
        model = models.LandUseClasses
        fields = (
            'co_cr',
            'co_funai',
            'map_year',
        )
