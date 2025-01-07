from django.db.models import Q
from rest_framework_simplejwt import authentication as jwt_authentication
from rest_framework import (
    permissions,
    authentication,
    exceptions
)


from layer import models


class LayerPermissionCheck(permissions.BasePermission):
    """Verify if user has layer permission."""

    def has_permission(self, request, view):
        """Verify if user has permission to request certain view.

        Args:
            request (DRF Request): User request.
            view (View class): View class.

        Raises:
            exceptions.PermissionDenied: Not authorized.

        Returns:
            bool: True
        """

        if request.user.is_anonymous:
            user_roles = []
        elif request.user.is_admin():
            return True
        else:
            user_roles = request.user.roles.all()

        layer_id = view.kwargs.get('id')

        queryset = models.Layer.objects.filter(id=layer_id)
        queryset = queryset.filter(
            Q(is_public=True) |
            Q(layer_permissions__groups__roles__in=user_roles)
        )
        if queryset.exists():
            return True
        raise exceptions.PermissionDenied(
            f"User does not have permission to access Layer {layer_id}."
        )


class VectorPermissionCheck(permissions.BasePermission):
    """Verify if user has vector permission."""

    def has_permission(self, request, view):
        """Verify if user has permission to request certain view.

        Args:
            request (DRF Request): User request.
            view (View class): View class.

        Raises:
            exceptions.PermissionDenied: Not authorized.

        Returns:
            bool: True
        """

        if request.user.is_anonymous:
            user_roles = []
        elif request.user.is_admin():
            return True
        else:
            user_roles = request.user.roles.all()

        vector_id = view.kwargs.get('id')

        queryset = models.VectorGeometry.objects.filter(id=vector_id)
        queryset = queryset.filter(
            Q(vector_uploaded__is_public=True) |
            Q(vector_uploaded__layer_permissions__groups__roles__in=user_roles)
        )
        if queryset.exists():
            return True
        raise exceptions.PermissionDenied(
            f"User does not have permission to access vector {vector_id}."
        )


class AdminRoleCheck(permissions.BasePermission):
    """Verify if user has admin role."""

    def has_permission(self, request, view):
        """Verify if user has permission to request certain view.

        Args:
            request (DRF Request): User request.
            view (View class): View class.

        Raises:
            exceptions.PermissionDenied: Not authorized.

        Returns:
            bool: True
        """

        if request.user.is_authenticated and request.user.is_admin():
            return True

        raise exceptions.PermissionDenied


class SafeRequestMethodCheck(permissions.BasePermission):
    """Verify if user has admin role or if it is a safe method."""

    def has_permission(self, request, view):
        """Verify if user has permission to request certain view.

        Args:
            request (DRF Request): User request.
            view (View class): View class.

        Raises:
            exceptions.PermissionDenied: Not authorized.

        Returns:
            bool: True
        """

        if request.user.is_authenticated and request.user.is_admin():
            return True
        # Allow safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        raise exceptions.PermissionDenied


class Auth:
    """Allow to access view only if authenticated."""

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (
        jwt_authentication.JWTAuthentication,
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )


class Public(Auth):
    """Allow any access to view (anyone)."""

    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()


class PublicAuth(Auth):
    """Allow any user authenticated access to view."""

    permission_classes = (permissions.AllowAny,)


class LayerAuth(Auth):
    """Verify if authenticated user also has permission to given layer."""

    permission_classes = (
        permissions.IsAuthenticated,
        LayerPermissionCheck,
        SafeRequestMethodCheck
    )


class PublicLayerAuth(Auth):
    """Verify if user has permission to given layer."""

    permission_classes = (
        permissions.AllowAny,
        LayerPermissionCheck,
        SafeRequestMethodCheck
    )


class PublicVectorAuth(Auth):
    """Verify if user has permission to given vector geometry."""

    permission_classes = (
        permissions.AllowAny,
        VectorPermissionCheck,
        SafeRequestMethodCheck
    )


class AdminAuth(Auth):
    """Allow to access view only if is admin."""

    permission_classes = (
        permissions.AllowAny,
        AdminRoleCheck
    )


class PublicSafeAuth(Auth):
    """Allow Public access view only on safe HTTP methods or if is an admin."""

    permission_classes = (
        permissions.AllowAny,
        SafeRequestMethodCheck
    )


class SafeAuth(Auth):
    """Allow to acess view only on safe HTTP methods or if is an admin."""

    permission_classes = (
        permissions.IsAuthenticated,
        SafeRequestMethodCheck
    )
