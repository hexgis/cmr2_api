from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
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
    """Returns the list of data in `models.DocsAction`."""

    queryset = models.DocsAction.objects.all().order_by('no_acao')
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

        actions_id_land_use = [11, 12, 13,]
        requested_action = self.request.GET.get('id_acao')
        requested_action = list(map(int,requested_action.split(',')))

        if all(item in actions_id_land_use for item in requested_action):
            return serializers.MapasUsoOcupacaoSoloSerializers
        elif not any(item in requested_action for item in
            actions_id_land_use):
            return serializers.DocumentosTISerializers
        else :
            raise exceptions.ParseError(
                "Não permitido retorno de dados de DocumentoTI"
                " UsoEOcupaçãoDoSolo na mesma requisição", None)

# class DocumentView(APIView):

#     http_method_names = ['post']
#     model = models.DocumentUpload
#     success_url = reverse_lazy('/')
#     parser_class = (FileUploadParser,)
#     permission_classes = [IsAuthenticated, ]

#     def post(self, request, *args, **kwargs):
#         file_serializer = serializers.DocumentUploadSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_serializer.save(user=self.request.user)
#             # save all fields 
#             dt_cadastro = request.data.get('dt_cadastro')
#             id_acao = request.data.get('id_acao')

#             return Response(file_serializer.data, 
#                 status=status.HTTP_201_CREATED)

#         else:
#             return Response(file_serializer.errors, 
#                 status=status.HTTP_400_BAD_REQUEST)


class DocumentUploadView(AuthModelMix, generics.GenericAPIView):

    def post(self, request):
        import pdb; pdb.set_trace()
        if request.method == 'POST' and request.FILES['arquivo']:
            instance = models.DocumentUpload(
                filee=request.FILES['arquivo'],
                # dt_cadastro=request.FILES['registration_date']
                # id_acao= 8
                # Para concluir essa demanda sera necessária código em 
                # code-review. Nesse trecho seram inseridos os atributos da 
                # nova Model do Documental modelada na 
                # branch "Feature/end points mapoteca".
                # Depois será removida a class DocumentUpload e associações.

            )
            instance.save()
            return Response("conteasdfnt", status=status.HTTP_200_OK)
        
        else:
            return Response("ERROR in request.", 
                status=status.HTTP_400_BAD_REQUEST)

