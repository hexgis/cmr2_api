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


class CatalogView2(AuthModelMixIn, generics.ListAPIView):
    """Returns catalogs data for the requested filter."""
    queryset = models.Catalog.objects.all()
    serializer_class = serializers.CatalogSerializer
    bbox_filter_field = 'geom'
    filterset_class = catalog_filters.CatalogFilter
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

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
        * if filter satellit is `sat_landsat8=LC08`
            `serializers.Landsat8CatalogSerializer` of data in
            `models.Landsat8Catalog`.
        * if filter satellit is `sat_sentinel2=Sentinel-2`
            `serializers.Sentinel2CatalogSerializer` of data in
            `models.Sentinel2Catalog`.
    """
    bbox_filter_field = 'geom'
    filterset_class = catalog_filters.CatalogsFilter
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

    def get_queryset(self):
        """Get method to return one data set acoording to satellite changed.

        Returns a satellite filtered model class in `views.CatalogView`.

        Returns:
            * satellite `Sentinel-2`:
                `models.Sentinel2Catalog`
            * satellite `LC08`:
                `models.Landsat8Catalog`
        """
        request_satellite = self.get_satellite_identifier()
        if request_satellite == "Sentinel-2":
            return models.Sentinel2Catalog.objects.all()
        elif request_satellite == "LC08":
            return models.Landsat8Catalog.objects.all()

    def get_serializer_class(self):
        """Get method to return one data set acoording to satellite changed.

        Returns one serializers class to `views.CatalogView`

        Returns:
            `serializers.Sentinel2CatalogSerializer` or
            `serializers.Landsat8CatalogSerializer`.
        """
        request_satellite = self.get_satellite_identifier()
        if request_satellite == "Sentinel-2":
            return serializers.Sentinel2CatalogSerializer
        elif request_satellite == "LC08":
            return serializers.Landsat8CatalogSerializer
        else:
            raise exceptions.ParseError(
                f"Satellite identify - {request_satellite} not defined!", None
            )

    def get_satellite_identifier(self):
        """Checks if the request satellite exists and 
        
        Returns the satellite identifier
        """
        request_satellite = str(self.request.GET.get('satellite'))
        satellite_selected = models.Satellite.objects.values("identifier").filter(
            identifier__exact = request_satellite).get()

        return satellite_selected['identifier']



















# sat_sentinel2 = models.Satellite.objects.values("identifier").filter(
#     identifier__exact = 'Sentinel-2').get()

