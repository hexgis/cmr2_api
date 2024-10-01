from django_filters import rest_framework

from catalog import models


class CharInFilter(
    rest_framework.BaseInFilter,
    rest_framework.CharFilter
):
    """Base class used for creating IN lookup filters to filter characters."""
    pass


class SceneFilters(rest_framework.FilterSet):
    """Django filter `models.Scene` data.

    Filters:
        * satellite (list_str): filtering Satellite using identify.
        * cloud_cover (number): filtering less than or equal for cloud values.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
    """
    satellite = CharInFilter(
        field_name='sat_identifier',
        lookup_expr='in',
        required=True,
    )

    cloud_cover = rest_framework.NumberFilter(
        field_name='cloud_cover',
        lookup_expr='lte',
    )

    start_date = rest_framework.DateFilter(
        field_name='date',
        lookup_expr='gte',
    )

    end_date = rest_framework.DateFilter(
        field_name='date',
        lookup_expr='lte',
    )

    class Meta:
        """Meta class for 'SceneFilters' filter."""
        model = models.Scene
        fields = (
            'satellite',
            'cloud_cover',
            'start_date',
            'end_date',
        )
