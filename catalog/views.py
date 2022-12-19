from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_gis import filters as gis_filters
from rest_framework import(
    generics,
    permissions
)

from catalog import (
    models,
    serializers,
    pagination,
    filters as catalog_filters
)


class AuthModelMixIn:
    """Default Authentication for catalog views."""
    permission_classes = (permissions.AllowAny,)


class SatelliteView(AuthModelMixIn, generics.ListAPIView):
    """Returns the list of satellites in `models.Satellite`."""

    queryset = models.Satellite.objects.all()
    serializer_class = serializers.SatelliteSerializer


class CatalogsView(AuthModelMixIn, generics.ListAPIView):
    """Returns catalogs data for the requested filter.

    Filters:
        *** satellite (list_str): filtering Satellite using identify. E.g.:
            LC08,
            Sentinel-2
        * cloud_cover (list): filtering less than or equal for cloud values.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """

    queryset = models.Catalogs.objects.all().order_by('sat')
    serializer_class = serializers.CatalogsSerializer
    bbox_filter_field = 'geom'
    filterset_class = catalog_filters.CatalogsFilter
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )
    pagination_class = pagination.CatalogoGeoJsonPagination