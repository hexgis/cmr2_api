from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (
    permissions,
    generics,
    exceptions
)

from documental import (
    models,
    serializers,
    filters as documental_filters
)


class AuthModelMix:
    """Default Authentication for priority_alerts views."""

    permission_class = (permissions.AllowAny,)


class ActionListView(AuthModelMix, generics.ListAPIView):
    """Returns the list of data in `models.DocsAction`."""

    queryset = models.DocsAction.objects.all().order_by('no_action')
    serializer_class = serializers.ActionListSerializers


class DocumentalListViews(AuthModelMix, generics.ListAPIView):
    """Returns `models.DocumentosDoc` data acoording to the selected actions.
    Filter:
        * id_acao (int) (mandatory): action identifier to be filtered.
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * map_year (list): filteringend years of the maps.
    """

    queryset = models.DocumentalDocs.objects.all().order_by('dt_registration')
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

        actions_id_land_use = {11, 12, 13}
        requested_action = self.request.GET.get('id_acao')
        requested_action = set(map(int, requested_action.split(',')))

        condiction_land_use = actions_id_land_use.copy()

        if len(condiction_land_use.union(requested_action).difference(actions_id_land_use)) == 0:
            return serializers.MapasUsoOcupacaoSoloSerializers
        elif actions_id_land_use.isdisjoint(requested_action):
            return serializers.DocumentosTISerializers
        else:
            raise exceptions.ParseError(
                "Não permitido retorno de documentos de DocumentoTI e"
                " UsoOcupaçãoDoSolo na mesma requisição", None)
