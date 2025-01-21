from rest_framework import serializers
from .models import LayerPermission, ComponentPermission
from layer.serializers import LayerSerializer
from layer.models import Layer

class LayerPermissionSerializer(serializers.ModelSerializer):
    layers = serializers.SerializerMethodField()
    layer_ids = serializers.PrimaryKeyRelatedField(
        queryset= Layer.objects.all(), 
        many=True, 
        write_only=True, 
        source='layers'
    ) 

    class Meta:
        model = LayerPermission
        fields = ['id', 'name', 'description', 'layers', 'layer_ids']
    
    def get_layers(self, obj):
        """Filtra os campos de layers retornados no serializer."""
        return obj.layers.values('id', 'name')


class ComponentPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentPermission
        fields = '__all__'
