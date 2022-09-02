from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import(
    generics,
    permissions,
    exceptions
)

from catalog import (
    models,
    serializers,
    filters as catalog_filters
)


class AuthModelMixIn:
    """Default Authentication for land_use views."""
    permission_classes = (permissions.AllowAny,)


class SatteliteView(AuthModelMixIn, generics.ListAPIView):
    queryset = models.Satellite.objects.all()
    serializer_class = serializers.SatteliteSerializer


class CatalogView(AuthModelMixIn, generics.ListAPIView):

    bbox_filter_field = 'geom'
    filterset_class = catalog_filters.CatalogFilter
    filter_backends = (DjangoFilterBackend,)

    sat_landsat8=2
    sat_sentinel2=3

    def get_queryset(self):
        request_satellite = int(self.request.GET.get('satellite'))
        if request_satellite == self.sat_sentinel2:
            print("sentinel2     ---->")
            return models.Sentinel2Catalog.objects.all()
        elif request_satellite == self.sat_landsat8:
            print("landsat8     ---->")
            return models.Landsat8Catalog.objects.all()

    def get_serializer_class(self):
        request_satellite = int(self.request.GET.get('satellite'))
        if request_satellite == self.sat_sentinel2:
            print("sentinel2")
            return serializers.Sentinel2CatalogSerializer
        elif request_satellite == self.sat_landsat8:
            print("landsat8")
            return serializers.Landsat8CatalogSerializer
        else:
            raise exceptions.ParseError(
                f"Satellite identify - {request_satellite} not defined!", None
            )
    


