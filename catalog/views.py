from rest_framework import(
    generics,
    permissions,
)

from catalog import (
    models,
    serializers,
)


class AuthModelMixIn:
    """Default Authentication for catalog views."""
    permission_classes = (permissions.AllowAny,)


class SatelliteView(AuthModelMixIn, generics.ListAPIView):
    """Returns the list of satellites in `models.Satellite`."""

    queryset = models.Satellite.objects.all()
    serializer_class = serializers.SatelliteSerializer