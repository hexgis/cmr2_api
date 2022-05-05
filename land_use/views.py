from django.shortcuts import render

from django.db.models import Sum, Count

from land_use import (
    models,
    serializers,
    filters as land_use_filters
)

from rest_framework import(generics, permissions)

from rest_framework_gis import filters as gis_filters


class AuthModelMixIn:
    """Default Authentication for monitoring views."""
    permission_classes = (permissions.AllowAny,)


class LandUseView(generics.ListAPIView):
    queryset = models.LandUseClasses
    serializer_class = serializers.LandUseSerializer


class LandUseYearsView(generics.ListAPIView):
    queryset = models.LandUseTI


class LandUseClassesView(generics.ListAPIView):
    queryset = models.LandUseClasses


class LandUseDetailView(generics.ListAPIView):
    queryset = models.LandUseClasses


class LandUseTableView(generics.ListAPIView):
    queryset = models.LandUseClasses


class LandUseStatesView(generics.ListAPIView):
    queryset = models.LandUseClasses
