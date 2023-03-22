from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_gis import filters as gis_filters
from rest_framework import (
    generics,
    permissions,
    response,
    exceptions
)
from auth_jwt import perm_access_cmr
from catalog import (
    models,
    serializers,
    pagination,
    filters as catalog_filters
)


# from django.contrib.auth.decorators import permission_required, login_required
# from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


class AuthModelMixIn:
    """Default Authentication for catalog views."""
    # permission_classes = (permissions.AllowAny,)
    permission_classes = (permissions.IsAuthenticated,)

class PossuiAcessoCMR(AuthModelMixIn):
    def tem_permicao_acesso_cmr(self):
        tem_permicao_cmr= perm_access_cmr.CMR_Modulo_Access.user_request_permission(self.request.user, __package__)
        return tem_permicao_cmr

class SatelliteView(PossuiAcessoCMR, generics.ListAPIView):
    """Returns the list of satellites in `models.Satellite`."""
    # queryset = models.Satellite.objects.all()
    serializer_class = serializers.SatelliteSerializer
    permission_required = ['catalog.view_satellite'] # 'catalog.veiw_catalogs_cmr_catalog'

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        if self.request.user.has_perms(perm_access_cmr.permis) and self.tem_permicao_acesso_cmr:
            queryset = models.Satellite.objects.all()
            print(perm_access_cmr.permis, self.request.user.has_perms(perm_access_cmr.permis),"\n Lucas Sena Alves \n")
            # import pdb; pdb.set_trace()
            return queryset
        else:
            raise exceptions.PermissionDenied


class SatelliteDetailView(AuthModelMixIn, generics.RetrieveAPIView):
    """Detail data for `deter_monitoring.models.DeterTI`.

    Filters:
        * pk (int): filtering request poligon identifier.
    """
    queryset = models.Satellite.objects.all()
    serializer_class = serializers.SatelliteSerializer
    lookup_field = 'pk'
    filter_backends = (DjangoFilterBackend,)




from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.decorators import api_view
from django.core.exceptions import ImproperlyConfigured



@api_view()
@permission_required('auth.add_user', raise_exception=True)
def firstFunc(request):
    print('messageDeu bom!!!\n\n', request.user, '\n\nlsa.view_satellitex: ', request.user.has_perm('lsa.view_satellitex'))
    # import pdb; pdb.set_trace()
    return response.Response({'message': "Deu bom!!!"})

class SatelliteXView(PermissionRequiredMixin, generics.ListAPIView):
    serializer_class = serializers.SatelliteSerializer
    permission_required = 'lsa.add_satellitex'
    # @permission_required('lsa.view_satellitex', raise_exception=True)
    def firstFuncc(self):
        print('messageDeu bom!!!\n\n', self.request.user, '\n\nlsa.view_satellitex: ', 
        self.request.user.has_perm('lsa.view_satellitex'))
        # import pdb; pdb.set_trace()
        return response.Response({'message': "Deu bom!!!"})
    def get_queryset(self):
        queryset = models.SatelliteX.objects.all()
        print(self.request.user.has_perm('lsa.view_satellitex'),"\n Lucas Sena Alves \n")
        # import pdb; pdb.set_trace()
        return queryset
    # def get_permission_required(self):
    #     perms = super(SatelliteXView, self).get_permission_required()
    #     print('self.fpermission_required')
    #     return perms   
    # def get_permission_required(self):
    #     return 'lsa.view_satellitex'
    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """
        # import pdb; pdb.set_trace()

        if self.permission_required is None:
            print('self1.permission_required')
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            print('self2.permission_required')
            # import pdb; pdb.set_trace()
            perms = (self.permission_required,)
        else:
            print('self3.permission_required')
            perms = self.permission_required
        return perms












class CatalogsView(AuthModelMixIn, generics.ListAPIView):
    """Returns catalogs data for the requested filter.

    Filters:
        *** satellite (list_str): filtering Satellite using identify. E.g.:
            LC08,
            Sentinel-2
        * cloud_cover (number): filtering less than or equal for cloud values.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """

    queryset = models.Catalogs.objects.all().order_by('sat_identifier')
    serializer_class = serializers.CatalogsSerializer
    bbox_filter_field = 'geom'
    filterset_class = catalog_filters.CatalogsFilters
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )
    pagination_class = pagination.CatalogGeoJsonPagination











# http://localhost:8080/land-use/?co_cr=30202001983&co_funai=11301&map_year=2019


# http://localhost:8080/monitoring/consolidated/table-stats/?grouping=monitoring_by_co_funai&co_cr=30202001913&co_funai=3002,7601&start_date=2017-06-24&end_date=2020-09-14

# http://localhost:8080/alerts/stats/?co_cr=30202001962&co_funai=20702&end_date=2021-05-09&start_date=2019-01-01

# http://localhost:8080/documental/list/?id_acao=8


