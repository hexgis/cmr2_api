from django.core.exceptions import ValidationError

from rest_framework import (
    views,
    status,
    generics,
    response
    )

from authorization import (
    constant,
    models,
    serializers
    )

from support import models as supportmodel

class LoggedUserPermissions(views.APIView):
    """Logged in user permissions."""

    def get(self, request, *args, **kwargs):
        """Lists all permissions associated to the logged in user."""
        return response.Response(request.user.get_all_permissions())


class LoggedUserCMRModules(views.APIView):
    """Logged in user access."""

    def get(self, request, *args, **kwargs):
        """Informs which 'CMR2 Modules' the logged in user has access to."""
        perms_cmrmodules = dict()

        for cmrmodules in list(constant.CMR_MODULES.keys()):
            perms_cmrmodules.update({cmrmodules: request.user.has_perms(constant.CMR_MODULES[cmrmodules]["access"])})

        return response.Response(perms_cmrmodules)
    

class CreatePermissionsView(generics.CreateAPIView):
    """ Loop to get every layer in support_layer and create a permission for them """
    serializer_class = serializers.UserPermssionsSerializer

    def create(self, request, *args, **kwargs):
        layer_query = supportmodel.Layer.objects.all()
        layer_data = [{"id": layer.id, "name": layer.name, "layers_g_id": layer.layers_group.id, "layers_g_name": layer.layers_group.name } for layer in layer_query]
        response_data = {
            "layers": layer_data,
        }
        for layer in layer_data:
            try:
                group_instance = supportmodel.LayersGroup.objects.get(id=layer['layers_g_id'])
                layer_instance = supportmodel.Layer.objects.get(id=layer['id'])
                models.PermissionsList.objects.get_or_create(
                    group_id = group_instance,
                    group_name = layer['layers_g_name'],
                    permission = "",
                    permission_name = "",
                    permission_layer_id = layer_instance,
                    permission_layer_name = layer['name'],
                    is_layer = True,
                )
            except ValidationError as e:
                return response.Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return response.Response(response_data, status=status.HTTP_201_CREATED)

