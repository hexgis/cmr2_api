from rest_framework import (
    generics,
    permissions,
    authentication,
    response,
    status
)
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters import rest_framework
from django.db.models import Q

from support import (
    models,
    serializers,
    filters as support_filters
)

from rolepermissions.checkers import has_permission
from rolepermissions.permissions import available_perm_status

from user_profile import models as userprofile_model
from authorization import models as authorizarion_model

class PublicAuthModelMixIn:
    """AuthModelMixIn default class for `support.views`."""
 
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )

class AuthModelMixIn:
    """AuthModelMixIn default class for `support.views`."""

    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.BasicAuthentication
    )
    permission_classes = (permissions.IsAuthenticated, )


class LayersGroupView(generics.ListAPIView, AuthModelMixIn):
    """Layers Group data view.

    Filters:
        * category (int): category group type
    """

    queryset = models.LayersGroup.objects.all()
    filterset_class = support_filters.LayersGroupFilter
    filter_backends = (rest_framework.DjangoFilterBackend,)

    def get_serializer_class(self):
        """Get method to return one data set according to authenticated user.

        Returns:
            `serializers.LayersGroupAuthenticatedSerializer` or
            `serializers.LayersGroupPublicSerializer`.
        """

        if self.request.user.is_authenticated:
            return serializers.LayersGroupAuthenticatedSerializer
        else:
            return serializers.LayersGroupPublicSerializer
        
    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            try:
                user_permissions = userprofile_model.UserPermission.objects.filter(user_id=user.id)
                allowed_layer_ids = []
                for perm in user_permissions:
                    permissions = authorizarion_model.PermissionsList.objects.filter(id=perm.permission_id)                
                    for id in permissions:
                        allowed_layer_ids.append(int(id.permission_layer_id.id))
                
                category_id = self.request.query_params.get('category')
                queryset = super().get_queryset().filter(category_groups=category_id)
                
                filtered_results = []
                for g in queryset:
                    layers = g.layers.filter(id__in=allowed_layer_ids)
                    if layers.exists():
                        filtered_results.append({
                        "id": g.id,
                        "name": g.name,
                        "order": g.order,
                        "layers": layers
                    })
            except Exception as e:
                return response.Response(f"An error occurred: {str(e)}", status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(filtered_results, many=True)
            return response.Response(serializer.data)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return response.Response(serializer.data)


class CategoryLayersGroupView(ListAPIView, AuthModelMixIn):
    """Category Layers Group data view."""

    queryset = models.CategoryLayersGroup.objects.all().order_by('name')
    serializer_class = serializers.CategoryLayersGroupSerializer


class LayersInfoView(ListAPIView, AuthModelMixIn):
    """Layers Info data view.

    Filters:
        * category (int): category group type
    """

    queryset = models.LayersInfo.objects.all()
    serializer_class = serializers.LayersInfoSerializer
