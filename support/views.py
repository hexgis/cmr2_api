from rest_framework import (
    generics,
    permissions,
    authentication
)
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters import rest_framework
from django.db.models import Q

from support import (
    models,
    serializers,
    filters as support_filters
)


class AuthModelMixIn:
    """AuthModelMixIn default class for `support.views`."""

    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )
    permission_classes = (permissions.IsAuthenticated, )


class LayersGroupView(ListAPIView, AuthModelMixIn):
    """Layers Group data view.

    Filters:
        * category (int): category group type
    """

    queryset = models.LayersGroup.objects.all()
    filterset_class = support_filters.LayersGroupFilter
    filter_backends = (rest_framework.DjangoFilterBackend,)

    def get_serializer_class(self):
        """Get method to return one data set acoording to authenticated user.

        Returns:
            `serializers.LayersGroupAuthenticatedSerializer` or
            `serializers.LayersGroupPublicSerializer`.
        """

        if self.request.user.is_authenticated:
            return serializers.LayersGroupAuthenticatedSerializer
        else:
            return serializers.LayersGroupPublicSerializer


class CategoryLayersGroupView(ListAPIView, AuthModelMixIn):
    """Category Layers Group data view."""

    queryset = models.CategoryLayersGroup.objects.all().order_by('name')
    serializer_class = serializers.CategoryLayersGroupSerializer


class LayersInfoView(ListAPIView, AuthModelMixIn):
    """Layers Info data view.

    Filters:
        * category (int): category group type
    """

    queryset = models.LayersInfo.objects.all()
    serializer_class = serializers.LayersInfoSerializer


class TiDetailView(ListAPIView):
    """
    View of Indigenous Land data presentation in geojson format for the application
    """
    serializer_class = serializers.GeoTerraIndigenaSerializer
    queryset = models.TerraIndigena.objects.all()


class TiByNameView(ListAPIView):
    """
    Presentation view for choosing the desired Indigenous Land
    """
    serializer_class = serializers.TiByNameSerializer

    def get_queryset(self):
        param = self.request.GET.get('param', None)
        queryset = models.TerraIndigena.objects.all()

        queryset = queryset.filter(
            Q(no_ti__icontains=param) |
            Q(no_municipio__icontains=param) |
            Q(co_cr__no_cr__icontains=param)
        )

        return queryset
