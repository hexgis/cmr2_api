from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication
)

from .models import (LayersGroup, CategoryLayersGroup)
from .serializers import (LayersGroupSerializer, CategoryLayersGroupSerializer)
from .filters import LayersGroupFilter


class AuthModelMixIn:
    """AuthModelMixIn default class for `support.views`."""

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )


class LayersGroupView(generics.ListAPIView, AuthModelMixIn):
    """ Layers Group data view.

    Filters:
        * category (int): catagoreis groups list
    """

    serializer_class = LayersGroupSerializer
    queryset = LayersGroup.objects.all()
    filterset_class = LayersGroupFilter
    filter_backends = (DjangoFilterBackend,)


class CategoryLayersGroupView(generics.ListAPIView, AuthModelMixIn):
    """Category Layers Group data view."""

    queryset = CategoryLayersGroup.objects.all().order_by('name')
    serializer_class = CategoryLayersGroupSerializer
