from django.db import models
from rest_framework.serializers import ModelSerializer

from funai import models


class LimiteTerraIndigenaSerializer (ModelSerializer):
    class Meta:
        model = models.LimiteTerraIndigena
        fields = '__all__'

class CoordenacaoRegionalSerializer (ModelSerializer):
    class Meta:
        model = models.CoordenacaoRegional
        fields = '__all__'