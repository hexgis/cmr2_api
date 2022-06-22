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


class DocumentosTIFilter(rest_framework.FilterSet):
    """Django filter `models.DocumentosTI` data.

    Filter:
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * start_date (str): filtering start date.
        * end_date (str): filteringend end date.
    """
    co_funai = NumberInFilter(
        field_name='co_funai',
        lookup_expr='in'
    )

    co_cr = CharInFilter(
        # field_name='co_cr',
        field_name='no_ti',
        lookup_expr='in'
    )

    start_date = rest_framework.DateFilter(
        field_name='dt_documento',
        lookup_expr='gte',
        required=False
    )

    end_date = rest_framework.DateFilter(
        field_name='dt_documento',
        lookup_expr='lte',
        required=False
    )
    
    class Meta:
        """Meta class for `AlertsFilter` filter."""
        model = models.DocumentosTI
        fields = (
            'co_funai',
            'co_cr',
            'start_date',
            'end_date',
        )


class MapasUsoOcupacaoSoloFilter(rest_framework.FilterSet):
    """Django filter `models.MapasUsoOcupacaoSolo` data.

    Filter:
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * start_date (str): filtering start date.
        * map_year (list): filteringend years of the maps.
    """
    co_funai = NumberInFilter(
        field_name='co_funai',
        lookup_expr='in'
    )

    # co_cr = CharInFilter(
    #     field_name='co_cr',
    #     lookup_expr='in'
    # )
    
    map_year = NumberInFilter(
        field_name='nu_ano',
        lookup_expr='in'
    )

    class Meta:
        """Meta class for `AlertsFilter` filter."""
        model = models.MapasUsoOcupacaoSolo
        fields = (
            'co_funai',
            'map_year',
        )
