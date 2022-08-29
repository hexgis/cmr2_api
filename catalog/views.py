from rest_framework import(
    generics,
    permissions,
)

from catalog import (
    models,
    serializers,
)

class AuthModelMixIn:
    """Default Authentication for land_use views."""
    permission_classes = (permissions.AllowAny,)

class SatteliteView(AuthModelMixIn, generics.ListAPIView):
    queryset = models.Sattelite.objects.all()
    serializer_class = serializers.SatteliteSerializer
