from django.db import models
from rest_framework.serializers import ModelSerializer

from priority_monitoring import models

class PriorityConsolidatedSerializer(ModelSerializer):

    class Meta:
        model= models.PriorityConsolidated
        fields= '__all__'

class PriorityConsolidatedTbSerializer(ModelSerializer):
    class Meta:
        models= models.PriorityConsolidatedTb
        fields= '__all__'