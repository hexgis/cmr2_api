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


class DocsActionFilter(rest_framework.FilterSet):
    """Django filter models.DocsAction data.

    Filter:
        * action_type (str): list action_id in action action_type filtered.
    """
    action_type = rest_framework.CharFilter(
        field_name='action_type',
        required=True,
    )

    class Meta:
        model = models.DocsAction
        fields = (
            'action_type',
        )


class DocumentalDocsFilter(rest_framework.FilterSet):
    """Django filter `models.DocumentalDocs` data.

    Filter:
        * id_acao (int): action identifier to be filtered.
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
    """
    id_acao = NumberInFilter(
        field_name='action_id',
        lookup_expr='in',
        # required=True,
    )

    co_cr = NumberInFilter(
        field_name='co_cr',
        lookup_expr='in',
    )

    co_funai = NumberInFilter(
        field_name='co_funai',
        lookup_expr='in',
    )

    class Meta:
        """Meta class for `DocumentalDocsFilter` filter."""
        model = models.DocumentalDocs
        fields = (
            'id_acao',
            'co_cr',
            'co_funai',
        )


class DocsDocumentTIFilter(DocumentalDocsFilter):
    """Django filter `models.DocsDocumentTI` data.

    Filter:
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
    """
    start_date = rest_framework.DateFilter(
        field_name='dt_document',
        lookup_expr='gte',
    )

    end_date = rest_framework.DateFilter(
        field_name='dt_document',
        lookup_expr='lte',
    )

    class Meta:
        """Meta class for `DocsDocumentTIFilter` filter."""
        model = models.DocsDocumentTI
        fields = (
            'start_date',
            'end_date',
        )


class DocsLandUserFilter(DocumentalDocsFilter):
    """Django filter `models.DocsLandUser` data.

    Filter:
        * map_year (list): filteringend years of the maps.
    """
    map_year = NumberInFilter(
        field_name='nu_year',
        lookup_expr='in',
    )

    class Meta:
        """Meta class for `DocsLandUserFilter` filter."""
        model = models.DocsLandUser
        fields = (
            'map_year',
        )
