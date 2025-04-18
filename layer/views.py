import base64

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

        # return serializers.GroupSerializer

    def get_queryset(self):
        queryset = models.Group.objects.all()

        # filter only groups that have layers:
        groups_ids = models.Layer.objects.values_list(
            'group',
            flat=True
        ).distinct()

        queryset = queryset.filter(id__in=groups_ids).distinct()

        # The loop that "cleans" null layers:
        for group in queryset:
            layers = group.layers.filter(
                Q(tms__isnull=False) | Q(wms__isnull=False)
            )
            group.layers.set(layers)

        return queryset.distinct()


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


class LayerThumbnailImageBase64View(mixins.PublicLayerAuth, views.APIView):
    """View to export layer thumbnail blob into base64 image."""

    def get(self, _, id):
        """Fetches the layer by identifier and returns the thumbnail image.

        Args:
            request (DRF Request): User request.
            id (str): Layer identifier.

        Returns:
            Response: Layer Thumbnail Image.
        """

        try:
            layer = models.Wms.objects.get(id=id)

            if not layer.thumbnail_blob:
                layer.save()

            img = base64.b64encode(layer.thumbnail_blob).decode('UTF-8')

            return response.Response(img, status.HTTP_200_OK)
        except Exception as exc:
            return response.Response(f'{exc}', status.HTTP_404_NOT_FOUND)


class LayerLegendImageBase64View(mixins.PublicLayerAuth, views.APIView):
    """View to export layer legend blob into base64 image."""

    def get(self, _, id):
        """Fetches the layer by identifier and returns the legend image.

        Args:
            request (DRF Request): User request.
            id (str): Layer identifier.

        Returns:
            Response: Layer Legend Image.
        """

        try:
            layer = models.Tms.objects.get(id=id)

            if not layer.legend_blob:
                layer.save()

            img = base64.b64encode(layer.legend_blob).decode('UTF-8')

            return response.Response(img, status.HTTP_200_OK)
        except Exception as exc:
            return response.Response(f'{exc}', status.HTTP_404_NOT_FOUND)
