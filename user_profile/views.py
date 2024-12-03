from django.shortcuts import render
from django.http import HttpResponseServerError
from django.contrib.gis.geos import GEOSGeometry, WKBWriter
from user_profile import models

from rest_framework.exceptions import NotFound

from rest_framework.exceptions import NotFound

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

from authorization import models as authorizationmodel
import json

import logging

logger = logging.getLogger(__name__)


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

class UserLoggetUpdateView (AuthModelMixIn, generics.UpdateAPIView):
    """
        View to update User settings.
    """
    serializer_class = serializers.UserSerializer
    queryset = models.UserSettings.objects.all()

    def patch(self, request, *args, **kwargs):
        user = request.user
        theme_mode = request.data.get('theme_mode')

        try:
            settings, created = models.UserSettings.objects.update_or_create(
                user=user,
                defaults={'dark_mode_active': theme_mode}
            )
            return response.Response("Settings successfully updated!", status=status.HTTP_200_OK)
        except models.UserSettings.DoesNotExist:
            return response.Response("User settings do not exist.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response(f"An error occurred: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


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


class UserUploadFileCreateView(
    AuthModelMixIn,
    generics.CreateAPIView
):
    """View to create `models.UserUploadedFileCreateView` data.

    Raises:
        Unauthenticated: User is not authenticated.

    Returns:
        dict: uploaded data.
    """

    serializer_class = serializers.UserUploadedFileSerializer  # Not in use

    def create(self, request):
        """Creates `UserUploadedFile` and its `UserUploadedFileGeometry`.

        Returns:
            dict: uploaded data with name, created_at, created and updated.
        """
        properties = request.data['geometry']['features'][0]['properties']
        try:
            user_upload, created = models.UserUploadedFile.objects.get_or_create(
                name=request.data.get('name'),
                user=request.user,
                is_active=True,
                properties=properties,
            )

            if created:
                logger.info(f"New UserUploadedFile created for user"
                            f"{request.user.username}.")
            else:
                logger.info(f"UserUploadedFile already exists for user "
                            f"{request.user.username}.")

        except Exception as e:
            logger.error(f"Error creating UserUploadedFile for user"
                         f"{request.user.username}: {e}"
                         )
            raise HttpResponseServerError(
                'Could not create file in the database.')

        created_data = 0
        data_exists = 0

        # Check for 'geometry' and 'features' in request data
        if 'geometry' not in request.data or 'features' not in request.data['geometry']:
            logger.error(
                "Invalid request data: 'geometry' or 'features' missing.")
            raise HttpResponseServerError(
                'Could not create file in the database. Invalid request data.')

        # Process each feature in geometry data
        for feature in request.data['geometry']['features']:
            try:
                geom = GEOSGeometry(str(feature['geometry']))

                # Ensure the geometry is 2D
                if geom.hasz:
                    geom = GEOSGeometry(WKBWriter(dim=2).write_hex(geom))

                # Create or get the geometry associated
                _, created = models.UserUploadedFileGeometry.objects.get_or_create(
                    user_uploaded=user_upload,
                    geom=geom,
                )

                if created:
                    created_data += 1
                    logger.info(
                        f"Created new geometry for UserUploadedFile ID"
                        f"{user_upload.id}.")
                else:
                    data_exists += 1
                    logger.info(f"Geometry already exists for UserUploadedFile ID "
                                f"{user_upload.id}.")

            except Exception as e:
                logger.error(f"Error creating geometries for UserUploadedFile ID "
                             f"{user_upload.id}: {e}")
                raise HttpResponseServerError(
                    f'Could not create geometries in the database: {e}')

        # Prepare the response data
        data = {
            'name': user_upload.name,
            'created_at': user_upload.date_created,
            'created': created_data,
            'updated': data_exists
        }

        logger.info(f"UserUploadedFile creation process completed for user "
                    f"{request.user.username}.")

        return response.Response(data, status=status.HTTP_201_CREATED)


class UserUploadFileDelete(
    AuthModelMixIn,
    generics.UpdateAPIView
):
    """View to update `models.UserUploadedFile` is_active status.

    Raises:
        Unauthenticated: User is not authenticated

    Returns:
        dict: User has been set as inactive.
    """

    serializer_class = serializers.UserUploadFileDeleteSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Returns queryset filtered by request user.

        Returns:
            Queryset: queryset list
        """

        return models.UserUploadedFile.objects.filter(
            user=self.request.user.id
        )


class UserUploadFileListGeometryView(AuthModelMixIn, generics.ListAPIView):
    """View to retrieve `models.UserUploadedFileGeometry` model data."""

    serializer_class = serializers.UserUploadedFileGeometryListSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Returns queryset filtered by request user.

        Returns:
            Queryset: queryset list
        """
        return models.UserUploadedFileGeometry.objects.filter(
            user_uploaded__user=self.request.user,
            user_uploaded__id=self.kwargs[self.lookup_field]
        )


class UserUploadFileGeometryDetailView(
    AuthModelMixIn,
    generics.RetrieveAPIView
):
    """View to retrieve `models.UserUploadedFileGeometry` model data.

    Raises:
        Unauthenticated: User is not authenticated

    Returns:
        dict: uploaded file data.
    """

    lookup_field = 'id'
    queryset = models.UserUploadedFileGeometry.objects.all()
    serializer_class = serializers.UserUploadedFileGeometryDetailSerializer


class GiverUserPermission(generics.CreateAPIView):
    """
    View to grant permissions to a user. This view handles the creation
    of user permissions based on the provided `permission` or `groups` IDs.
    """

    serializer_class = serializers.UserPermissionSerializer

    def create(self, request, *args, **kwargs):
        try:
            usr = self.request.user
            permissions_ids = request.data.get('permission')
            group_permissions_ids = request.data.get('groups')

            # Process group permissions if provided
            if group_permissions_ids:
                for group_id in group_permissions_ids:
                    groups_instances = authorizationmodel.PermissionsList.objects.filter(
                        group_id=group_id)

                    if groups_instances.exists():
                        for groups_instance in groups_instances:
                            models.UserPermission.objects.update_or_create(
                                user=usr,
                                permission=groups_instance
                            )
                    else:
                        return response.Response(f"No User Permissions found for group_id {group_id}", status=status.HTTP_404_NOT_FOUND)

            # Process individual permissions if provided
            if permissions_ids:
                for perm in permissions_ids:
                    permission_instance = authorizationmodel.PermissionsList.objects.get(
                        permission_layer_id=perm)
                    models.UserPermission.objects.update_or_create(
                        user=usr,
                        permission=permission_instance
                    )
                    return response.Response(f"Permissões concedidas com sucesso para o usuário {usr}", status=status.HTTP_201_CREATED)

        except Exception as e:
            return response.Response(f"An error occurred: {str(e)}", status=status.HTTP_400_BAD_REQUEST)

        return response.Response(f"Permissões concedidas com sucesso para o usuário {usr}", status=status.HTTP_201_CREATED)


class UserUploadFileUpdatePropertiesPatchView(AuthModelMixIn, generics.UpdateAPIView):
    """
    View to update `properties` field of `models.UserUploadedFile`.

    Raises:
        Unauthenticated: User is not authenticated.

    Returns:
        dict: Updated properties.
    """
    serializer_class = serializers.UserUploadedFileSerializer
    lookup_field = 'id'

    def get_object(self):
        """Get the `UserUploadedFile` object."""
        try:
            uploaded_file_id = self.request.data.get('id')
            if not uploaded_file_id:
                raise HttpResponseServerError(
                    'ID is required in the request body'
                )

            return models.UserUploadedFile.objects.get(
                user=self.request.user,
                id=uploaded_file_id
            )
        except models.UserUploadedFile.DoesNotExist:
            raise NotFound('Uploaded file not found')

    def patch(self, request, *args, **kwargs):
        """Update `color` in `properties` of `UserUploadedFile`."""
        uploaded_file = self.get_object()

        try:
            color = request.data.get('color')
            name = request.data.get('name')

            if color is not None:
                # Update or initialize the properties field
                properties = uploaded_file.properties or {}
                properties['color'] = color
                uploaded_file.properties = properties
                uploaded_file.save()

            if name is not None:
                uploaded_file.name = name
                uploaded_file.save()

            data = {
                'id': uploaded_file.id,
                'properties': uploaded_file.properties,
                'name': uploaded_file.name
            }

            return response.Response(data, status=status.HTTP_200_OK)

        except Exception as exc:
            raise HttpResponseServerError(
                f'Could not update properties in database: {str(exc)}'
            )
