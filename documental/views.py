from rest_framework import (
    permissions,
    generics
)

from documental import (
    models, 
    serializers
)


class AuthModelMix:
    """Default Authentication for priority_alerts views."""
    permission_class = (permissions.AllowAny,)


class ActionListView(generics.ListAPIView):
    """Returns the list of data in `models.Action`."""
    queryset = models.Action.objects.all().order_by('no_acao')
    serializer_class = serializers.ActionListSerializers


class DocumentalDocsViews(generics.ListAPIView):
    """Returns `models.DocumentosDoc` data acoording to the selected actions.
    Filter:
        * acao_id (integer) (mandatory): action identifier to be filtered
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * start_date (str): filtering start date.
        * end_date (str): filteringend end date.
    """
    queryset = models.DocumentalDocs.objects.all().order_by('dt_cadastro')
    serializer_class = serializers.MapasUsoOcupacaoSoloSerializers
    filterset_class = documental_filters.DocumentalDocsFilter
    filter_backends = DjangoFilterBackend,
    