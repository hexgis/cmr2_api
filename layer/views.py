from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError
from django.db.models import Q

from rest_framework import (
    generics,
    response,
    status,
    views
)

from permission import mixins
from layer import (
    models,
    serializers,
    filters
)


class GroupsCreateListView(mixins.PublicSafeAuth, generics.ListCreateAPIView):
    """Layer Group view creates list and data."""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.GroupFilter

    def get_serializer_class(self):
        """Gets serializer class for `models.Group`

        Returns:
            serializer_class (type): layers serializer class.
        """

        # if 'simple' in self.request.query_params.keys():
        #     return serializers.GroupSimpleSerializer
        # if 'complete' in self.request.query_params.keys():
        return serializers.GroupCompleteSerializer

        return serializers.GroupSerializer

    def get_queryset(self):
        """Gets Queryset for `models.Group`.

        Returns:
            Queryset: filtered queryset.
        """

        queryset = models.Group.objects.all()
        if 'simple' in self.request.query_params.keys():
            return queryset

        # Removes groups that do not have layers
        groups = models.Layer.objects.all().values('group')
        queryset = queryset.filter(id__in=groups)

        # Filter null layers
        for group in queryset:
            layers = group.layers.filter(
                Q(tms__isnull=False) | Q(wms__isnull=False))
            group.layers.set(layers)

        return queryset


class GroupsUpdateDeleteView(
    mixins.AdminAuth,
    generics.RetrieveUpdateDestroyAPIView
):
    """Class for delete and update Group data."""

    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    lookup_field = 'id'

    def destroy(self, request, id):
        """Method to verify Group deletion.

        Args:
            request (DRF Request): User request.

        Raises:
            IntegrityError: Layers Group linked the registered layer.

        Returns:
            response: Invalid or correct response for delete layers group.
        """

        instance = self.get_object()

        try:
            instance.delete()
        except IntegrityError:
            return response.Response(
                {"error": "Layers Group linked the registered layer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return response.Response(status=status.HTTP_204_NO_CONTENT)


class LayerListView(mixins.Public, generics.ListAPIView):
    def get_serializer_class(self):
        """Gets serializer class for `models.Layer`."""
        return serializers.LayerSerializer

    def get_queryset(self, *args, **kwargs):
        """Returns the queryset for layers."""
        return models.Layer.objects.select_related('group').all() 
    
    def get_serializer(self, *args, **kwargs):
        """Customize the serializer to include specific fields."""
        kwargs['fields'] = ('id', 'name', 'group_name') 
        return super().get_serializer(*args, **kwargs)