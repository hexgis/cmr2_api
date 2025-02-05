from rest_framework import generics
from .models import LayerPermission, ComponentPermission
from .serializers import LayerPermissionSerializer, ComponentPermissionSerializer
from permission.mixins import AdminAuth, Public

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from layer import models as layer_model
from layer import serializers as layer_serializer

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

class LayerPermissionView(Public, APIView):
    """
    View to manage layer permissions

    Methods:
    - GET: Return the layers permissions.
    - POST: Create a new permission layer.
    - PATCH: Update partially a layer permission.
    """

    def get(self, request, pk=None):
        """
        List all permissions layer or return a specific permission.

        Args:
            pk (int, opcional): ID permission.
        """
        if pk:
            try:
                permission = LayerPermission.objects.get(pk=pk)               
            except LayerPermission.DoesNotExist:
                return Response({'detail': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = LayerPermissionSerializer(permission)
            return Response(serializer.data, status=status.HTTP_200_OK)

        permissions = LayerPermission.objects.all()
        serializer = LayerPermissionSerializer(permissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ Create a new permission layer"""
        
        serializer = LayerPermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """ Update partially a layer permission."""
        
        try:
            permission = LayerPermission.objects.get(pk=pk)
        except LayerPermission.DoesNotExist:
            return Response({'detail': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LayerPermissionSerializer(permission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LayerPermissionDiffView(Public, APIView):
    """ returns the difference between the layers that are not in the permission """
    def get(self, request, pk, *args, **kwargs):
        try:
            layer_permission = LayerPermission.objects.get(pk=pk)
        except LayerPermission.DoesNotExist:
            raise NotFound({"detail": "LayerPermission não encontrada."})

        permission_layer_ids = list(layer_permission.layers.values_list('id', flat=True))

        layer_ids = list(layer_model.Layer.objects.values_list('id', flat=True))

        diff_ids = [id_ for id_ in layer_ids if id_ not in permission_layer_ids]

        layers = layer_model.Layer.objects.filter(id__in=diff_ids).select_related('group')
        serializer = layer_serializer.LayerSerializer(
            layers, many=True, fields=('id', 'name', 'group_name')
        )

        return Response(serializer.data)