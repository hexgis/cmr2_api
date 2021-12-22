from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer

from priority_monitoring.models import PriorityConsolidated, PriorityConsolidatedTb

class PriorityConsolidatedSerializer (ModelSerializer):

    class Meta:
        model= PriorityConsolidated
        fields= '__all__'

class PriorityConsolidatedTbSerializer (ModelSerializer):
    class Meta:
        models:PriorityConsolidatedTb
        fields= '__all__'