from django.shortcuts import render
from django.http import Http404
from django.contrib.gis.geos import GEOSGeometry, WKBWriter
from user_profile import models

from rest_framework_simplejwt import authentication as jwt_authentication
from rest_framework import (
    authentication,
    response,
    permissions,
    status,
    generics,
    views,
)

from user_profile import (
    serializers
)


class AuthModelMixIn:
    """"Authentication Model MixIn for UserProfile views.

    Default authentication_classes for JWT, Token and Session Authentication.
    Default permission_classes for permissions.IsAuthenticated.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (
        jwt_authentication.JWTAuthentication,
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )


# class UserRequest(AuthModelMixIn, views.APIView):
#     """View for handling user print requests."""

#     queryset = models.User.objects.all()
#     serializer_class = serializers.UserSerializer

class UserLoggedGetView(AuthModelMixIn, generics.GenericAPIView):
    """View to post User logs.

    Returns:
        dict: Serialized user logs model
    """

    serializer_class = serializers.UserSerializer

    def get(self, request) -> response.Response:
        """Get user logged data.

        Returns:
            response.Response: returns serialized data from requested user.
        """

        serializer = self.serializer_class(request.user)
        return response.Response(serializer.data)


class UserUploadFileListView(
    AuthModelMixIn,
    generics.ListAPIView
):
    """View to retrieve `models.UserUploadedFile` model data.

    Raises:
        Unauthenticated: User is not authenticated

    Returns:
        dict: uploaded file data.
    """

    serializer_class = serializers.UserUploadedFileSerializer

    def get_queryset(self):
        """Returns queryset filtered by request user and is_active status.

        Returns:
            Queryset: queryset list
        """

        return models.UserUploadedFile.objects.filter(
            user=self.request.user.id, is_active=True
        )
