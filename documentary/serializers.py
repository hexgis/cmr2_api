from rest_framework import serializers

from documentary import models


class ActionListSerializers(serializers.ModelSerializer):
    """Serializer for return list actions `models.Action` data."""
    class Meta:
        """Meta class for `ActionListSerializers` serializer."""
        model = models.Action
        fields = (
            'id',
            'no_acao',
        )