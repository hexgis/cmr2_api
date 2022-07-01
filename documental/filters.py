from django_filters import rest_framework

from documental import models

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


class DocumentalDocsFilter(rest_framework.FilterSet):
    """Django filter `models.DocumentalDocs` data.

    Filter:
        * acao_id (int): action identifier to be filtered.
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * map_year (list): filteringend years of the maps.
    """
    
    acao_id = CharInFilter(
        field_name='acao_id',
        lookup_expr='in',
        required=True
    )
    
    co_cr = NumberInFilter(
        field_name='co_cr',
        lookup_expr='in'
    )

    co_funai = NumberInFilter(
        field_name='co_funai',
        lookup_expr='in'
    )

    start_date = rest_framework.DateFilter(
        field_name='dt_documento',
        lookup_expr='gte'
    )

    end_date = rest_framework.DateFilter(
        field_name='dt_documento',
        lookup_expr='lte'
    )

    map_year = NumberInFilter(
        field_name='nu_ano',
        lookup_expr='in'
    )

    class Meta:
        """Meta class for `DocumentalDocsFilter` filter."""
        model = models.DocumentalDocs
        fields = (
            'acao_id',
            'co_cr',
            'co_funai',
            'start_date',
            'end_date',
            'map_year',
        )       