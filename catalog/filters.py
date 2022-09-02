from django_filters import rest_framework

from catalog import models


class CatalogFilter(rest_framework.FilterSet):
    
    satellite = rest_framework.NumberFilter(
        field_name='satellite',
        lookup_expr='exact',
        required=True,
    )

    percent_cloud = rest_framework.NumberFilter(
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
        model = models.Catalogs
        fields = ['start_date', 'end_date', 'percent_cloud']