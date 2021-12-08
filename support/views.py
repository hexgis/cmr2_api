from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication
)

from .models import LayersGroup
from .serializers import LayersGroupSerializer


class AuthModelMixIn:
    """ AuthModelMixIn default class for `support.views` """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )


class LayersGroupView(generics.ListAPIView, AuthModelMixIn):
    """ Layers Group data view """

    queryset = LayersGroup.objects.all()
    serializer_class = LayersGroupSerializer
