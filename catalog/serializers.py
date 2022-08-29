from rest_framework import serializers

from catalog import models


class SatteliteSerializer(serializers.ModelSerializer):
    """Serializer to return registered sattelites."""

    class Meta:
        """Meta Class for `catalog.SatteliteSerializer` serializer."""
        model = models.Sattelite
        fields = (
            'identifier',
            'name',
        )