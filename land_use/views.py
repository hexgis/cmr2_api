from django.db.models import Sum, Count

from land_use import (
    models,
    serializers,
    filters as land_use_filters
)

from django_filters import rest_framework
from rest_framework_gis import filters as gis_filters
from rest_framework import (
    generics,
    permissions,
    response,
    status
)


class AuthModelMixIn:
    """Default Authentication for land_use views."""
    permission_classes = (permissions.AllowAny,)


class LandUseView(AuthModelMixIn, generics.ListAPIView):
    """Returns the list of `models.LandUseClasses` spatial data.

    Filters:
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenous Lands using Funai code.
        * map_year (list): filtering years mapped in land use mapping.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """
    queryset = models.LandUseClasses.objects.all()
    serializer_class = serializers.LandUseSerializer
    bbox_filter_field = 'geom'
    filterset_class = land_use_filters.LandUseClassesFilter
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


class LandUseDetailView(AuthModelMixIn, generics.RetrieveAPIView):
    """Returns detailed data for a queried element of `models.LandUseClasses` data.

    Filters:
        * id (int): filtering request poligon identifier.
    """
    queryset = models.LandUseClasses.objects.all()
    serializer_class = serializers.LandUseDetailSerializer
    lookup_field = 'id'


class LandUseStatsView(AuthModelMixIn, generics.ListAPIView):
    """Retrives `models.LandUseClasses` stats data.

    Filters:
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenous Lands using Funai code.
        * map_year (list): filtering years mapped in land use mapping.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """
    queryset = models.LandUseClasses.objects.all()
    serializer_class = serializers.LandUseSerializer
    filterset_class = land_use_filters.LandUseClassesFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

    def get(self, request):
        """Get method to return stats for land_use APP.

        Returns sums for area_ha, area_km2 and registry.

        Args:
            request (Requests.request): Request data.

        Returns:
            response.Response: django rest_framework.Response.response api response data.
        """
        data = self.filter_queryset(self.queryset).aggregate(
            area_ha=Sum('nu_area_ha'),
            area_km2=Sum('nu_area_km2'),
            total=Count('id')
        )
        return response.Response(data, status=status.HTTP_200_OK)


class LandUseTabletView(generics.ListAPIView):
    """
    ListAPIView for LandUsePerTi with filtering capabilities.
    """
    queryset = models.LandUsePerTi.objects.all()
    serializer_class = serializers.LandUseTableSerializer
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )
    filterset_class = land_use_filters.LandUsePerTiFilter


class LandUsePerTiSearchListView(generics.ListAPIView):
    """
    ListAPIView for LandUsePerTi with filtering capabilities.
    """
    queryset = models.LandUsePerTi.objects.all().distinct()
    serializer_class = serializers.LandUseSearchSerializer
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )
    filterset_class = land_use_filters.LandUsePerTiFilter
