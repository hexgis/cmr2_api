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
    """Returns the list of data in `models.DocsAction`.

    Filter:
        * action_type (str): list action_id in action action_type filtered.
    """
    queryset = models.DocsAction.objects.all()
    serializer_class = serializers.ActionListSerializers
    filterset_class = documental_filters.DocsActionFilter
    filter_backends = (DjangoFilterBackend,)


class DocumentalListViews(AuthModelMix, generics.ListAPIView):
    """Return three data set acoording to the selected actions in the request.

    * In the type of action of the category `DOCUMENTS_TI`:
        Data contained in `models.DocsDocumentTI`.
        Use the `serializers.DocsDocumentTISerializers` serializer.
        Applied filters:
            * id_acao (int) (mandatory): action identifier to be filtered.
            * co_cr (list): filtering Regional Coordination using code.
            * co_funai (list): filtering Indigenou Lands using Funai code.
            * start_date (str): filtering start date.
            * end_date (str): filtering end date.

    * In tht type of action of the category `MAPS_LAND_USER`:
        Data contained in `models.DocsLandUser`.
        Use the `serializers.DocsLandUserSerializers` serializer.
        Applied filters:
            * id_acao (int) (mandatory): action identifier to be filtered.
            * co_cr (list): filtering Regional Coordination using code.
            * co_funai (list): filtering Indigenou Lands using Funai code.
            * map_year (list): filteringend years of the maps.

    * In the type of action of the category `MAPOTECA`:
        Data contained in `models.DocsMapoteca`.
        Use the `serializers.DocsMapotecaSerializers` serializer.
        Applied filters:
            * id_acao (int) (mandatory): action identifier to be filtered.
            * co_cr (list): filtering Regional Coordination using code.
            * co_funai (list): filtering Indigenou Lands using Funai code.
    """

    filter_backends = (DjangoFilterBackend,)
    filterset_class = documental_filters.DocumentalDocsFilter

    def get_action_type(self):
        """Return only one aciton type according to actions sent in request"""
        requested_action = list(map(int, self.request.GET.get('id_acao').split(',')))
        # requested_action = self.request.GET.get('id_acao')
        # import pdb; pdb.set_trace()
        
        # requested_action = list(map(int, requested_action.split(',')))

        action_type_docs = models.DocsAction.objects.values(
            'action_type').filter(id_action__in=requested_action).distinct()

        if action_type_docs.count() == 1:
            return str(action_type_docs[0]['action_type'])
        elif not action_type_docs.exists():
            raise exceptions.ParseError(
                "TIPO DE AÇÃO não registrada. Informe uma ação válida.", None)
        else:
            raise exceptions.ParseError(
                "Não permitido retorno de dados com mais de uma TIPO DE AÇÃO"
                " na mesma requisição.", None)

    def get_serializer_class(self):
        """Get method to return one data set acoording to action category.

        Returns one serializers class to `views.DocumentalListViews`

        Returns:
            `serializers.DocsDocumentTISerializers` or
            `serializers.DocsLandUserSerializers` or
            `serializers.DocsMapotecaSerializers`.
        """

        action_type_docs = self.get_action_type()

        if action_type_docs == "DOCUMENTS_TI":
            return serializers.DocsDocumentTISerializers
        elif action_type_docs == "MAPS_LAND_USER":
            return serializers.DocsLandUserSerializers
        elif action_type_docs == "MAPOTECA":
            return serializers.DocsMapotecaSerializers

    def get_queryset(self):
        """Get method to return one data set acoording to action category.

        Returns one models class and filter `views.DocumentalListViews`.

        Returns:
            * Category `DOCUMENTS_TI`:
                `models.DocsDocumentTI`
                `documental_filters.DocsDocumentTIFilter`
            * Category `MAPS_LAND_USER`:
                `models.DocsLandUser`
                `documental_filters.DocsLandUserFilter`
            * Category `MAPOTECA`:
                `models.DocsMapoteca`
                `documental_filters.DocumentalDocsFilter`.
        """
        action_type_docs = self.get_action_type()

        if action_type_docs == "DOCUMENTS_TI":
            self.filterset_class = documental_filters.DocsDocumentTIFilter
            return models.DocsDocumentTI.objects.all()
        elif action_type_docs == "MAPS_LAND_USER":
            self.filterset_class = documental_filters.DocsLandUserFilter
            return models.DocsLandUser.objects.all()
        elif action_type_docs == "MAPOTECA":
            return models.DocsMapoteca.objects.all()
        else:
            raise exceptions.ParseError(
                "ERROR in the data set returned", None)
