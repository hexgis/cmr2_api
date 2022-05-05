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


class LandUseMappingView(generics.ListAPIView):
    queryset = models.LandUseMappingClasses
    serializer_class = serializers.LandUseMappingSerializer


class LandUseMappingYearsView(generics.ListAPIView):
    queryset = models.LandUseMappingTI


class LandUseMappingClassesView(generics.ListAPIView):
    queryset = models.LandUseMappingClasses


class LandUseMappingDetailView(generics.ListAPIView):
    queryset = models.LandUseMappingClasses


class LandUseMappingTableView(generics.ListAPIView):
    queryset = models.LandUseMappingClasses


class LandUseMappingStatesView(generics.ListAPIView):
    queryset = models.LandUseMappingClasses
