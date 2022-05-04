from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication
)

from .models import (LayersGroup, CategoryLayersGroup)
from .serializers import (LayersGroupSerializer, CategoryLayersGroupSerializer)


class AuthModelMixIn:
    """ AuthModelMixIn default class for `support.views` """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )


class LayersGroupView(generics.ListAPIView, AuthModelMixIn):
    """ Layers Group data view """

    lookup_field = 'id'
    serializer_class = LayersGroupSerializer

    def get_queryset(self):
        id = self.kwargs[self.lookup_field]
        return LayersGroup.objects.filter(category_groups=id)


class CategoryLayersGroupView(generics.ListAPIView, AuthModelMixIn):
    """_Category Layers Group data view """

    queryset = CategoryLayersGroup.objects.all().order_by('name')
    serializer_class = CategoryLayersGroupSerializer
