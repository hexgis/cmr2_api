from rest_framework import serializers
from .models import LayerPermission, ComponentPermission
from layer.models import Layer
from user.models import Group
from user.models import Role


class LayerPermissionSerializer(serializers.ModelSerializer):
    layers = serializers.SerializerMethodField()
    layer_ids = serializers.PrimaryKeyRelatedField(
        queryset=Layer.objects.all(),
        many=True,
        write_only=True,
        source='layers'
    )

    class Meta:
        model = LayerPermission
        fields = ['id', 'name', 'description', 'layers', 'layer_ids']

    def get_layers(self, obj):
        """
            Returns a list of dictionaries containing 'id', 'name', and 'group_name' 
            for each Layer associated with the LayerPermission object.

            Args:
                obj (LayerPermission): The LayerPermission instance.

            Returns:
                list: A list of dictionaries with layer details.
        """

        layers = obj.layers.prefetch_related(
            'group'
        )

        return [
            {
                'id': layer.id,
                'name': layer.name,
                'group_name': layer.group.name if layer.group else None
            }
            for layer in layers
        ]


class ComponentPermissionSerializer(serializers.ModelSerializer):
    """
        Serializer for the ComponentPermission model, returning all fields.
    """
    class Meta:
        model = ComponentPermission
        fields = '__all__'


class GroupSimpleSerializer(serializers.ModelSerializer):
    """
        Serializer for the Group model, returning only 'id' and 'name' fields.
    """
    class Meta:
        model = Group
        fields = ('id', 'name')


class RoleWithGroupsSerializer(serializers.ModelSerializer):
    """
        Serializer for the Role model, including related groups using GroupSimpleSerializer.
    """
    groups = GroupSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'groups')
