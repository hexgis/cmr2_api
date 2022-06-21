from rest_framework import (
    permissions,
    generics
)

from documentary import (
    models, 
    serializers
)


class AuthModelMix:
    permission_class = (permissions.AllowAny,)


class ActionListVeiw(generics.ListAPIView):
    queryset = models.Action.objects.all().order_by('no_acao')
    serializer_class = serializers.ActionListSerializers

