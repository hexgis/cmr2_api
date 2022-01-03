from django.db import models
from rest_framework.serializers import ModelSerializer

from priority_monitoring import models

class PriorityConsolidatedTempSerializer(ModelSerializer):
    class Meta:
        model= models.PriorityConsolidatedTemp
        fields= '__all__'

class PriorityConsolidatedSerializer(ModelSerializer):
    class Meta:
        models= models.PriorityConsolidated
        fields= '__all__'