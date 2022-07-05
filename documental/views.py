from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (
    permissions,
    generics
)

from documental import (
    models,
    serializers,
    filters as documental_filters
)


class AuthModelMix:
    """Default Authentication for priority_alerts views."""

    permission_class = (permissions.AllowAny,)


class ActionListView(generics.ListAPIView):
    """Returns the list of data in `models.DocsAction`."""

    queryset = models.DocsAction.objects.all().order_by('no_acao')
    serializer_class = serializers.ActionListSerializers


class DocumentalListViews(generics.ListAPIView):
    """Returns `models.DocumentosDoc` data acoording to the selected actions.
    Filter:
        * id_acao (int) (mandatory): action identifier to be filtered.
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * map_year (list): filteringend years of the maps.
    """

    queryset = models.DocumentalDocs.objects.all().order_by('dt_cadastro')
    filterset_class = documental_filters.DocumentalDocsFilter
    filter_backends = (DjangoFilterBackend,)
    
    def get_serializer_class(self):
        """Get method to return data acoording to the action category selected
        in the `models.DocumentosDoc` data.

        Returns one serializers class to `views.ActionListView`
        
        Returns:
            `serializers.MapasUsoOcupacaoSoloSerializers` or
            `serializers.DocumentosTISerializers`.
        """

        actions_id_land_use = ['11', '12', '13']
        error_mensag = 'Action not defined in your request.'
        requested_action = str(self.request.GET.get('id_acao', error_mensag))

        if requested_action in actions_id_land_use:
            return serializers.MapasUsoOcupacaoSoloSerializers
        else:
            return serializers.DocumentosTISerializers