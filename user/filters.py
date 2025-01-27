from django_filters.rest_framework import (
    FilterSet,
    BooleanFilter
)

from user import models


class UserUploadFileFilter(FilterSet):
    """FilterSet model used to filter Sentinel2Scene data from view.

    Filters:
        start_date (str): start date in YYYY-MM-DD.
        end_date (str): end date in YYYY-MM-DD.
        cloud_cover (float): cloud cover percentage.
    """

    is_active = BooleanFilter(field_name='is_active')

    class Meta:
        """Metaclass for Sentinel2SceneFilter."""

        model = models.UserUploadedFile
        fields = '__all__'
