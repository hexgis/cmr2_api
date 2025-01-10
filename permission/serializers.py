from rest_framework import serializers
from .models import LayerPermission, ComponentPermission


class LayerPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerPermission
        fields = '__all__'


class ComponentPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentPermission
        fields = '__all__'
