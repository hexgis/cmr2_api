from inspect import CO_COROUTINE

from django_filters import rest_framework

from land_use import models


class NumberInFilter(
    rest_framework.NumberFilter,
    rest_framework.BaseInFilter
):
    pass


class LandUseClassesFilter(rest_framework.FilterSet):
    co_cr = NumberInFilter(
        field_name='co_cr',
        lookup_expr='in'
    )

    co_funai = NumberInFilter(
        field_name='co_funai',
        lookup_expr='in'
    )

    year_map = NumberInFilter(
        field_name='nu_ano',
        lookup_expr='in'
    )

    class Meta:
        model = models.LandUseClasses
        fields = (
            'co_cr',
            'co_funai',
            'year_map',
        )
