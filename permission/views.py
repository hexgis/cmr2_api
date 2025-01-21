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
    View para gerenciar permissões de camadas.

    Métodos:
    - GET: Retorna todas as permissões de camadas.
    - POST: Cria uma nova permissão de camada.
    - PATCH: Atualiza parcialmente uma permissão de camada.
    """

    def get(self, request):
        """
        Lista todas as permissões de camada.

        Returns:
            Response: Lista de permissões.
        """
        permissions = LayerPermission.objects.all()
        serializer = LayerPermissionSerializer(permissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Cria uma nova permissão de camada.

        Args:
            request (Request): Dados para criar a permissão.

        Returns:
            Response: Permissão criada ou erros de validação.
        """
        serializer = LayerPermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Atualiza parcialmente uma permissão de camada.

        Args:
            request (Request): Dados para atualizar a permissão.
            pk (int): ID da permissão.

        Returns:
            Response: Permissão atualizada ou erros de validação.
        """
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