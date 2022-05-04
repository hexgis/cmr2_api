from django_filters import rest_framework

from support import models


class LayersGroupFilter (rest_framework.FilterSet):
    """LayersGroupFilter data.

    Filters:
        category (int): catagoreis groups list
    """
    category = rest_framework.NumberFilter(
        field_name='category_groups',
        lookup_expr='exact'
    )

    class Meta:
        """Metaclass to 'support.LayersGroupFilter'."""
        model = models.LayersGroup
        fields = ('category',)
