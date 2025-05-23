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
        """
        Retorna os campos 'id', 'name' e 'group_name' para cada Layer.
        """
        layers = obj.layers.select_related('group')  # Otimiza a consulta para incluir o grupo
        return [
            {
                'id': layer.id,
                'name': layer.name,
                'group_name': layer.group.name if layer.group else None  # Pega o nome do grupo
            }
            for layer in layers
        ]


class ComponentPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentPermission
        fields = '__all__'
