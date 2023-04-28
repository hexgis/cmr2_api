from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis import filters as gis_filters

from rest_framework import (
    generics,
    permissions,
    exceptions
)

from authorization.permissions import perm_access_cmr
from catalog import (
    models,
    serializers,
    pagination,
    filters as catalog_filters
)


class AuthModelMixIn:
    """Default Authentication for catalog views."""
    permission_classes = (permissions.IsAuthenticated,)


class HasAcessCMR(AuthModelMixIn):
    """Management of the first level of access to the CMR Modules."""
    def has_perm_access_cmr(self):
        """Validates if the logged in user has the necessary permissions to
        access the CMR Modules in this APP."""
        tem_permicao_cmr = perm_access_cmr.CMRModuleAccess.user_request_permission(
            self.request.user, __package__)
        return tem_permicao_cmr


class SatelliteView(HasAcessCMR, generics.ListAPIView):
    """Returns the list of satellites in `models.Satellite`."""
    serializer_class = serializers.SatelliteSerializer

    def get_queryset(self):
        """Returns the set of data according to access and permissions granted
        to the logged in user"""
        if self.request.user.has_perm('catalog.view_satellite') and self.has_perm_access_cmr():
            return models.Satellite.objects.all()
        else:
            raise exceptions.PermissionDenied


class SceneView(HasAcessCMR, generics.ListAPIView):
    """Returns Scene data for the requested filter.

    Filters:
        ** satellite (list_str): filtering Satellite using identify. E.g.:
            LC08,
            Sentinel-2
        * cloud_cover (number): filtering less than or equal for cloud values.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """
    serializer_class = serializers.SceneSerializer
    bbox_filter_field = 'geom'
    filterset_class = catalog_filters.SceneFilters
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )
    pagination_class = pagination.CatalogGeoJsonPagination

    def get_queryset(self):
        """Returns the set of data according to access and permissions granted
        to the logged in user"""
        if self.request.user.has_perms('catalog.view_Scene') and self.has_perm_access_cmr():
            return models.Scene.objects.all().order_by('sat_identifier')
        else:
            raise exceptions.PermissionDenied
