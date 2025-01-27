from rest_framework import generics
from .models import LayerPermission, ComponentPermission
from .serializers import LayerPermissionSerializer, ComponentPermissionSerializer
from permission.mixins import AdminAuth


class LayerPermissionListView(AdminAuth, generics.ListAPIView):
    """
    Retorna a lista de todos os LayerPermission.
    """
    queryset = LayerPermission.objects.all()
    serializer_class = LayerPermissionSerializer


class ComponentPermissionListView(AdminAuth, generics.ListAPIView):
    """
    Retorna a lista de todos os ComponentPermission.
    """
    queryset = ComponentPermission.objects.all()
    serializer_class = ComponentPermissionSerializer
