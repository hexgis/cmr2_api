from django.shortcuts import render

from django.db.models import Sum, Count

from land_use import (
    models,
    serializers,
    filters as land_use_filters
)

from django_filters import rest_framework
from rest_framework_gis import filters as gis_filters
from rest_framework import(
    generics,
    permissions
)


class AuthModelMixIn:
    """Default Authentication for monitoring views."""
    permission_classes = (permissions.AllowAny,)


class LandUseTableView(generics.ListAPIView):
    queryset = models.LandUseTI.objects.all()
    serializer_class = serializers.LandUseTableSerializer
    filterset_class = land_use_filters.LandUseTIFilter
    filter_backends = (rest_framework.DjangoFilterBackend,)


class LandUseView(generics.ListAPIView):
    queryset = models.LandUseTI.objects.all()
    serializers_class = serializers.LandUseSerializer
    filterset_class = land_use_filters.LandUseTIFilter
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


class LandUseDetailView(generics.RetrieveAPIView):
    queryset = models.LandUseTI.objects.all()
    serializers_class = serializers.LandUseDetailSerializer
    lookup_field = 'id'
    filter_backends = (rest_framework.DjangoFilterBackend,)


class LandUseYearsView(generics.ListAPIView):
    queryset = models.LandUseTI.objects.distinct('no_ano')
    serializers_class = serializers.LandUseYearsSerializer
    fiterset_class = land_use_filters.LandUseTIFilter
    filter_backends = (rest_framework.DjangoFilterBackend,)


class LandUseClassesView(generics.ListAPIView):
    queryset = models.LandUseClasses.objects.distinct('no_estagio')
    serializers_class = serializers.LandUseClassesSerializer


class LandUseStatesView(generics.ListAPIView):
    queryset = models.LandUseTI.objects.all()
    serializers_class = serializers.LandUseStatesserializer
    filterset_class = land_use_filters.LandUseTIFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

    def get(self, request):
        data = self.filter_queryset(self.queryset).aggregate(
            area_ha=Sum('nu_area_ha'),
            area_km2=Sum('nu_area_km2'),
            total=Count('id')
        )
