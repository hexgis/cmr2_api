from rest_framework import generics
from .models import LayerPermission, ComponentPermission
from .serializers import LayerPermissionSerializer, ComponentPermissionSerializer
from permission.mixins import AdminAuth
from drf_spectacular.utils import extend_schema, OpenApiExample

class LayerPermissionListView(AdminAuth, generics.ListAPIView):
    """
    Retorna a lista de todos os LayerPermission.
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
    Retorna a lista de todos os ComponentPermission.
    """
    queryset = ComponentPermission.objects.all()
    serializer_class = ComponentPermissionSerializer
