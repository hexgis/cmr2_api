from rest_framework import (
    generics,
    permissions,
    authentication
)
from django_filters import rest_framework

from support import (
    models,
    serializers,
    filters as support_filters
)


class AuthModelMixIn:
    """AuthModelMixIn default class for `support.views`."""

    authentication_classes = (
        authentication.SessionAuthentication, authentication.BasicAuthentication
    )
    permission_classes = (permissions.IsAuthenticated, )


class LayersGroupView(generics.ListAPIView, AuthModelMixIn):
    """Layers Group data view.

    Filters:
        * category (int): category group type
    """

    serializer_class = serializers.LayersGroupSerializer
    queryset = models.LayersGroup.objects.all()
    filterset_class = support_filters.LayersGroupFilter
    filter_backends = (rest_framework.DjangoFilterBackend,)


class CategoryLayersGroupView(generics.ListAPIView, AuthModelMixIn):
    """Category Layers Group data view."""

    queryset = models.CategoryLayersGroup.objects.all().order_by('name')
    serializer_class = serializers.CategoryLayersGroupSerializer
