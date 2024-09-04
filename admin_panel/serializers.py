from rest_framework import serializers
from admin_panel import models

class InstitutionSerailizer(serializers.ModelSerializer):
    class Meta:
        model = models.Institutions
        fields = '__all__'