from django.db import models
from rest_framework.serializers import ModelSerializer

from priority_monitoring.models import PriorityConsolidated

class PriorityConsolidatedSerializer (ModelSerializer):

    class Meta:
        model= PriorityConsolidated
        fields= '__all__'
