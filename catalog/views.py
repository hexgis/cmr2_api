from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_gis import filters as gis_filters

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
    """Default Authentication for catalog views."""
    permission_classes = (permissions.AllowAny,)


class SatelliteView(AuthModelMixIn, generics.ListAPIView):
    """Returns the list of satellites in `models.Satellite`."""

    queryset = models.Satellite.objects.all()
    serializer_class = serializers.SatelliteSerializer


class CatalogView(AuthModelMixIn, generics.ListAPIView):
    """Returns the models list of existing catalogs for the requested filter.

    Filters:
        * satellite (list): filtering Satellite using identify.
        * cloud_cover (list): filtering less than or equal for cloud values.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).

    Returns:
        * if filter satellit is `sat_landsat8=2`
            `serializers.Landsat8CatalogSerializer` of data in 
            `models.Landsat8Catalog`.
        * if filter satellit is `sat_sentinel2=3`
            `serializers.Sentinel2CatalogSerializer` of data in 
            `models.Sentinel2Catalog`.
    """

    bbox_filter_field = 'geom'
    filterset_class = catalog_filters.CatalogFilter
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

    sat_landsat8 = models.Satellite.objects.values("identifier").filter(
        identifier__exact = 'LC08').get()
    sat_sentinel2 = models.Satellite.objects.values("identifier").filter(
        identifier__exact = 'Sentinel-2').get()

    def get_queryset(self):
        request_satellite = str(self.request.GET.get('satellite'))

        if request_satellite == self.sat_sentinel2['identifier']:
            return models.Sentinel2Catalog.objects.all()
        elif request_satellite == self.sat_landsat8['identifier']:
            return models.Landsat8Catalog.objects.all()

    def get_serializer_class(self):
        request_satellite = str(self.request.GET.get('satellite'))

        if request_satellite == self.sat_sentinel2['identifier']:
            return serializers.Sentinel2CatalogSerializer
        elif request_satellite == self.sat_landsat8['identifier']:
            return serializers.Landsat8CatalogSerializer
        else:
            raise exceptions.ParseError(
                f"Satellite identify - {request_satellite} not defined!", None
            )
