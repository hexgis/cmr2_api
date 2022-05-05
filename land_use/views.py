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


class LandUseView(generics.ListAPIView):
    queryset = models.LandUseClasses.objects.all()
    serializer_class = serializers.LandUseSerializer
    filterset_class = land_use_filters.LandUseClassesFilter
    filter_backends = (rest_framework.DjangoFilterBackend,)


class LandUseGeoView(generics.ListAPIView):
    queryset = models.LandUseClasses.objects.all()
    serializers_class = serializers.LandUseGeomSerializer
    filterset_class = land_use_filters.LandUseClassesFilter
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


class LandUseDetailView(generics.RetrieveAPIView):
    queryset = models.LandUseClasses.objects.all()
    serializers_class = serializers.LandUseDetailSerializer
    lookup_field = 'id'
    filter_backends = (rest_framework.DjangoFilterBackend,)


class LandUseYearsView(generics.ListAPIView):
    queryset = models.LandUseClasses.objects.distinct('no_ano')
    serializers_class = serializers.LandUseYearsSerializer
    fiterset_class = land_use_filters.LandUseClassesFilter
    filter_backends = (rest_framework.DjangoFilterBackend,)


class LandUseClassesView(generics.ListAPIView):
    queryset = models.LandUseClasses


class LandUseTableView(generics.ListAPIView):
    queryset = models.LandUseClasses


class LandUseStatesView(generics.ListAPIView):
    queryset = models.LandUseClasses
