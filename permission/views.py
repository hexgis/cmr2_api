from rest_framework import generics
from .models import LayerPermission, ComponentPermission
from .serializers import RoleWithGroupsSerializer, LayerPermissionSerializer, ComponentPermissionSerializer
from permission.mixins import AdminAuth, Public

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from layer import models as layer_model
from layer import serializers as layer_serializer

from permission.mixins import AdminAuth
from drf_spectacular.utils import extend_schema, OpenApiExample
from user.models import Role, Group
from user import (
    serializers,
)


class GroupPermissionListView(AdminAuth, generics.ListAPIView):
    """
        Returns the list of all LayerPermissions.
    """

    queryset = Role.objects.all()
    serializer_class = RoleWithGroupsSerializer


class LayerPermissionListView(AdminAuth, generics.ListAPIView):
    """
        Returns the list of all LayerPermission.
    """

    queryset = LayerPermission.objects.all()
    serializer_class = LayerPermissionSerializer

    @extend_schema(
        summary="Lista de LayerPermission",
        description="Retorna todas as permissões de camadas cadastradas no sistema.",
        responses={
            200: LayerPermissionSerializer(many=True),
            403: {"description": "Permissão negada."},
        },
        examples=[
            OpenApiExample(
                "Exemplo de Resposta",
                value=[
                    {
                        "id": 1,
                        "name": "PLANET",
                        "description": "Permissão para acessar todas as imagens Planet.",
                        "layers": [1]
                    },
                    {
                        "id": 2,
                        "name": "Acesso Restrito",
                        "description": "conjunto de funcionalidades que os usuários tem acesso quando sua solicitação de acesso restriro é aprovada pelo gestor.",
                        "components": ["layers", "monitoring", "layers_mosaics", "land_use", "analytics", "admin_panel"]
                    }
                ],
                response_only=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ComponentPermissionListView(AdminAuth, generics.ListAPIView):
    """
        Returns the list of all ComponentPermission.
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

        serializer = LayerPermissionSerializer(
            permission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LayerPermissionDiffView(Public, APIView):
    """ 
        Returns the difference between the layers that are not in the permission 
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            layer_permission = LayerPermission.objects.get(pk=pk)
        except LayerPermission.DoesNotExist:
            raise NotFound({"detail": "LayerPermission não encontrada."})

        permission_layer_ids = list(
            layer_permission.layers.values_list('id', flat=True))

        layer_ids = list(
            layer_model.Layer.objects.values_list('id', flat=True))

        diff_ids = [id_ for id_ in layer_ids if id_ not in permission_layer_ids]

        layers = layer_model.Layer.objects.filter(
            id__in=diff_ids).select_related('group')
        serializer = layer_serializer.LayerSerializer(
            layers, many=True, fields=('id', 'name', 'group_name')
        )

        return Response(serializer.data)


class RoleGroupDiffView(Public, APIView):
    """
        Returns groups that are not yet associated with a given role.
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            raise NotFound({"detail": "Role não encontrada."})

        associated_group_ids = list(role.groups.values_list('id', flat=True))
        all_group_ids = list(Group.objects.values_list('id', flat=True))

        diff_ids = [
            id_ for id_ in all_group_ids if id_ not in associated_group_ids]

        groups = Group.objects.filter(id__in=diff_ids)
        serializer = serializers.GroupSerializer(groups, many=True)

        return Response(serializer.data)


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

        serializer = LayerPermissionSerializer(
            permission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LayerPermissionDiffView(Public, APIView):
    """ 
        Returns the difference between the layers that are not in the permission 
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            layer_permission = LayerPermission.objects.get(pk=pk)
        except LayerPermission.DoesNotExist:
            raise NotFound({"detail": "LayerPermission não encontrada."})

        permission_layer_ids = list(
            layer_permission.layers.values_list('id', flat=True))

        layer_ids = list(
            layer_model.Layer.objects.values_list('id', flat=True))

        diff_ids = [id_ for id_ in layer_ids if id_ not in permission_layer_ids]

        layers = layer_model.Layer.objects.filter(
            id__in=diff_ids).select_related('group')
        serializer = layer_serializer.LayerSerializer(
            layers, many=True, fields=('id', 'name', 'group_name')
        )

        return Response(serializer.data)
