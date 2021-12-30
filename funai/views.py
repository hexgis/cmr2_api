# from django.shortcuts import render
from rest_framework import generics
from django.db.models.query import QuerySet

from funai import(
    serializers,
    models
)


class CoordenacaoRegionalView (generics.ListAPIView):
    queryset = models.CoordenacaoRegional.objects.all()
    serializer_class = serializers.CoordenacaoRegionalSerializer

class LimiteTerraIndigenaView (generics.ListAPIView):
    queryset = models.LimiteTerraIndigena.objects.all()
    serializer_class = serializers.LimiteTerraIndigenaSerializer

# class CrTiFunai (generics.ListAPIView):
#     models.LimiteTerraIndigena
#     models.CoordenacaoRegional