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

    queryset = models.DocsAction.objects.all()
    serializer_class = serializers.ActionListSerializers
    filterset_class = documental_filters.DocsActionFilter


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

    filter_backends = (DjangoFilterBackend,)
    filterset_class = documental_filters.DocumentalDocsFilter

    def get_action_type(self):
        """Função get_action_type"""

        requested_action = self.request.GET.get('id_acao')
        requested_action = list(map(int, requested_action.split(',')))

        action_type_docs = models.DocsAction.objects.values(
            'action_type').filter(id_action__in=requested_action).distinct()

        if action_type_docs.count() == 1:
            return str(action_type_docs[0]['action_type'])
        else:
            raise exceptions.ParseError(
                "Não permitido retorno de dados com mais de uma TIPO DE AÇÃO"
                " na mesma requisição ou TIPO DE AÇÃO não registrada", None)

    def get_serializer_class(self):
        """Get method to return data acoording to the action category selected
        in the `models.DocumentosDoc` data.

        Returns one serializers class to `views.ActionListView`

        Returns:
            `serializers.MapasUsoOcupacaoSoloSerializers` or
            `serializers.DocumentosTISerializers`.
        """

        action_type_docs = self.get_action_type()

        if action_type_docs == "DOCUMENTS_TI":
            return serializers.DocsDocumentTISerializers
        elif action_type_docs == "MAPS_TI":
            return serializers.DocsLandUserSerializers
        elif action_type_docs == "MAPOTECA":
            return serializers.DocsMapotecaSerializers

    def get_queryset(self):
        """Função get_queryset """

        action_type_docs = self.get_action_type()

        if action_type_docs == "DOCUMENTS_TI":
            self.filterset_class = documental_filters.DocsDocumentTIFilter
            return models.DocsDocumentTI.objects.all()
        elif action_type_docs == "MAPS_TI":
            self.filterset_class = documental_filters.DocsLandUserFilter
            return models.DocsLandUser.objects.all()
        elif action_type_docs == "MAPOTECA":
            return models.DocsMapoteca.objects.all()
        else:
            raise exceptions.ParseError(
                "XPTO Não permitido retorno de dados com mais de uma TIPO DE AÇÃO"
                " na mesma requisição", None)
