from django_filters import rest_framework

from catalog import models


class CharInFilter(
    rest_framework.BaseInFilter,
    rest_framework.CharFilter
):
    """Base class used for creating IN lookup filters to filter characters."""
    pass


class CatalogsFilter(rest_framework.FilterSet):
    """Django filter `models.Catalogs` data.

    Filters:
        * satellite (list_str): filtering Satellite using identify.
        * cloud_cover (list): filtering less than or equal for cloud values.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
    """
    satellite = CharInFilter(
        field_name='sat_id__identifier',
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
        """Meta class for 'CatalogsFilter' filter."""
        model = models.Catalogs
        fields = (
            'satellite',
            'cloud_cover',
            'start_date',
            'end_date',
        )
