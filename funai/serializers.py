from django.db import models
from rest_framework.serializers import ModelSerializer

from funai import models


class LimiteTerraIndigenaSerializer (ModelSerializer):
    """LimiteTerraIndigenaSerializer data"""

    class Meta:
        model = models.LimiteTerraIndigena
        fields = (
            'co_funai',
            'no_ti'
        )


class CoordenacaoRegionalSerializer (ModelSerializer):
    class Meta:
        model = models.CoordenacaoRegional
        fields = (
            'co_cr',
            'no_cr'
        )
