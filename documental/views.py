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


