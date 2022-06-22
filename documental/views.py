import imp
from rest_framework import (
    permissions,
    generics
)

from documental import (
    models, 
    serializers,
    filters
)


class AuthModelMix:
    permission_class = (permissions.AllowAny,)


class ActionListView(generics.ListAPIView):
    queryset = models.Action.objects.all().order_by('no_acao')
    serializer_class = serializers.ActionListSerializers


