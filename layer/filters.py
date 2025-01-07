from django.db.models import Q
from django_filters.rest_framework import FilterSet

from layer import models


class GroupFilter(FilterSet):
    """Layer Group FilterSet class."""

    @property
    def qs(self):
        """Filter the queryset based on user roles.

        Args:
            queryset (QuerySet): The queryset to filter.

        Returns:
            QuerySet: The filtered queryset based on user roles.
        """

        queryset = super().qs

        if 'category' in self.request.query_params.keys():
            category_id = self.request.query_params.get('category')
            queryset = queryset.filter(
                layers__group__category_groups=category_id
            )

        if 'initial' in self.request.query_params.keys():
            queryset = queryset.filter(
                layers__active_on_init=True
            ).distinct('id').order_by('id')

        if self.request.user.is_anonymous:
            user_roles = []
        elif self.request.user.is_admin():
            return queryset
        else:
            user_roles = self.request.user.roles.all()

        return queryset.filter(
            Q(layers__is_public=True) |
            Q(layers__layer_permissions__groups__roles__in=user_roles)
        ).distinct('id').order_by('id')

    class Meta:
        """Meta class for GroupFilter."""

        model = models.Group
        fields = '__all__'


class LayerFilter(FilterSet):
    """Layer FilterSet class."""

    @property
    def qs(self):
        """Filter the queryset based on user roles.

        Args:
            queryset (QuerySet): The queryset to filter.

        Returns:
            QuerySet: The filtered queryset based on user roles.
        """

        queryset = super().qs

        if 'initial' in self.request.query_params.keys():
            queryset = queryset.filter(
                active_on_init=True
            ).distinct('id').order_by('id')

        if self.request.user.is_anonymous:
            user_roles = []
        elif self.request.user.is_admin():
            return queryset
        else:
            user_roles = self.request.user.roles.all()

        return queryset.filter(
            Q(is_public=True) |
            Q(layer_permissions__groups__roles__in=user_roles)
        ).distinct('id').order_by('id')

    class Meta:
        """Meta class for LayerFilter."""

        model = models.Layer
        fields = ('id',)


class VectorGeometryFilter(FilterSet):
    """Vector Geometry FilterSet class."""

    @property
    def qs(self):
        """Filter the queryset based on name parameter.

        Args:
            queryset (QuerySet): The queryset to filter.

        Returns:
            QuerySet: The filtered queryset based on name parameter.
        """

        queryset = super().qs
        if 'name' in self.request.query_params.keys():
            queryset = queryset.filter(
                properties__name__icontains=self.request.query_params['name']
            )

        return queryset

    class Meta:
        """Meta class for VectorGeometryFilter."""

        model = models.VectorGeometry
        fields = ('vector_uploaded',)


class VectorFilter(FilterSet):
    """Vector FilterSet class."""

    class Meta:
        """Meta class for VectorFilter."""

        model = models.Vector
        fields = ('type',)
