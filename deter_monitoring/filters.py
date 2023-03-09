from django_filters import rest_framework

from deter_monitoring import models


class NumberInFilter(
    rest_framework.BaseInFilter,
    rest_framework.NumberFilter
):
    """Base class used for creating IN lookup filters to filter numbers."""
    pass


class CharInFilter(
    rest_framework.BaseInFilter,
    rest_framework.CharFilter
):
    """Base class used for creating IN lookup filters to filter characters."""
    pass


class DeterTIFilters(rest_framework.FilterSet):
    """DeterTIFilters data.

    Filters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code
        * stage (list_str): Classification classes. E.g.:
            "CICATRIZ_DE_QUEIMADA"; "DESMATAMENTO_VEG"; "CS_DESORDENADO";
            "DESMATAMENTO_CR"; "CS_GEOMETRICO"; "DEGRADACAO"; "MINERACAO"
        * satellite (list_str): filtering Satellite using identify.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
    """
    co_cr = NumberInFilter(
        field_name='co_cr',
        lookup_expr='in'
    )

    co_funai = NumberInFilter(
        field_name='co_funai',
        lookup_expr='in'
    )

    stage = CharInFilter(
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
        """Meta class for `DeterTIFilters` filter."""
        model = models.DeterTI
        fields = (
            'co_cr',
            'co_funai',
            'stage',
            'satellite',
            'start_date',
            'end_date'
        )
