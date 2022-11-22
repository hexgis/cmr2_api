from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import (
    FileUploadParser, MultiPartParser, FormParser)
from rest_framework.views import APIView
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework import status

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

        requested_action = self.request.GET.get('id_acao')
        requested_action = requested_action.split(',')
        requested_action = list(map(int, requested_action))

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


class DocumentUploadView(generics.ListCreateAPIView):
    """View to upload the files and their attributes `models.DocsDocumentTI`.
    id_acao
    """

    def get_serializer_class(self):
        """Get method to return one data set acoording to action category.

        Returns:
            `serializers.DocsDocumentTIUploadSerializers` or
            `serializers.DocsLandUserUploadSerializers` or
            `serializers.DocsMapotecaUploadSerializers`.
        """

        action_type_docs = self.get_action_typee()

        if action_type_docs == "DOCUMENTS_TI":
            return serializers.DocsDocumentTIUploadSerializers
        elif action_type_docs == "MAPS_LAND_USER":
            return serializers.DocsLandUserUploadSerializers
        elif action_type_docs == "MAPOTECA":
            return serializers.DocsMapotecaUploadSerializers

    def get_action_typee(self):
        """Return only one aciton type according to actions sent in request"""

        requested_action = self.request.GET.get('id_acao')
        requested_action = requested_action.split(',')
        requested_action = list(map(int, requested_action))
        action_type_docs = models.DocsAction.objects.values(
            'action_type').filter(id_action__in=requested_action).distinct()

        if action_type_docs.count() == 1:
            return str(action_type_docs[0]['action_type'])
        elif not action_type_docs.exists():
            raise exceptions.NotFound(
                "TIPO DE AÇÃO não registrada. Informe uma ação válida.", None)
        else:
            raise exceptions.ParseError(
                "Não permitido retorno de dados com mais de uma TIPO DE AÇÃO"
                " na mesma requisição.", None)

    def upload_file(self, request):
        """Upload the dataset to add DOCUMENTS_TI file to the DOCUMENTS_TI.

        Returns:
            dict: upload dataset.
        """
        action_type_docs = self.get_action_typee()

        if request.method == 'POST':
            if action_type_docs == "DOCUMENTS_TI":
                serializer = serializers.DocsDocumentTIUploadSerializers(
                    request.POST, request.FILES)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(
                        file=request.FILES['file'],
                        action_id=request.GET.get('id_acao'),
                        id_document=request.data['id_document'],
                        path_document=request.data['path_document'],
                        no_document=request.data['no_document'],
                        usercmr_id=request.data['usercmr_id'],
                        st_availablest_available=request.data['st_available'],
                        st_excludedst_excluded=request.data['st_excluded'],
                        dt_registration=request.data['dt_registration'],
                        dt_update=request.data['dt_update'],
                        co_funai=request.data['co_funai'],
                        no_ti=request.data['no_ti'],
                        co_cr=request.data['co_cr'],
                        ds_cr=request.data['ds_cr'],
                        dt_document=request.data['dt_document'],
                        no_extension=request.data['no_extension'],
                    )
                    return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif action_type_docs == "MAPS_LAND_USER":
                serializer = serializers.DocsLandUserUploadSerializers(
                    request.POST, request.FILES)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(
                        file=request.FILES['file'],
                        action_id=request.GET.get('id_acao'),
                        id_document=request.data['id_document'],
                        path_document=request.data['path_document'],
                        no_document=request.data['no_document'],
                        usercmr_id=request.data['usercmr_id'],
                        st_availablest_available=request.data['st_available'],
                        st_excludedst_excluded=request.data['st_excluded'],
                        dt_registration=request.data['dt_registration'],
                        dt_update=request.data['dt_update'],
                        co_funai=request.data['co_funai'],
                        no_ti=request.data['no_ti'],
                        co_cr=request.data['co_cr'],
                        ds_cr=request.data['ds_cr'],
                        nu_year=request.data['nu_year'],
                        nu_year_map=request.data['nu_year_map']
                    )
                    return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif action_type_docs == "MAPOTECA":
                serializer = serializers.DocsMapotecaUploadSerializers(
                    request.POST, request.FILES)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(
                        file=request.FILES['file'],
                        action_id=request.GET.get('id_acao'),
                        id_document=request.data['id_document'],
                        path_document=request.data['path_document'],
                        no_document=request.data['no_document'],
                        usercmr_id=request.data['usercmr_id'],
                        st_availablest_available=request.data['st_available'],
                        st_excludedst_excluded=request.data['st_excluded'],
                        dt_registration=request.data['dt_registration'],
                        dt_update=request.data['dt_update'],
                        co_funai=request.data['co_funai'],
                        no_ti=request.data['no_ti'],
                        co_cr=request.data['co_cr'],
                        ds_cr=request.data['ds_cr'],
                        no_description=request.data['no_description'],
                        map_dimension=request.data['map_dimension'],
                        js_ti=request.data['js_ti']
                    )
                    return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                raise exceptions.ParseError(
                    "ERROR in the data set returned", None)

        else:
            return Response("ERROR in request.", status=status.HTTP_400_BAD_REQUEST)
