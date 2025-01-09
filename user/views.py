from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import os
import logging

from django.http import Http404
from django.contrib.gis.geos import GEOSGeometry, WKBWriter
from django_filters.rest_framework import DjangoFilterBackend
from permission.mixins import Auth, Public, AdminAuth
from django.http import HttpResponseServerError
from django.template.loader import render_to_string

from rest_framework_gis.filters import InBBoxFilter
from .serializers import AccessRequestSerializer
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.conf import settings
from rest_framework import (
    response,
    status,
    generics,
    views,
)


from user import (
    serializers,
    models,
    filters
)

logger = logging.getLogger(__name__)


class UserListView(Auth, generics.ListCreateAPIView):
    """"API to return all users along with their respective sector ID.

    Returns:
        queryset: user and sector_id queryset
    """

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserLoggedGetView(Auth, generics.GenericAPIView):
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


class UserUploadFileGeometryDetailView(
    Auth,
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


class UserUploadFileListCreateView(Auth, generics.ListCreateAPIView):
    """Basemap view creates list and data."""

    serializer_class = serializers.UserUploadedFileSerializer
    queryset = models.UserUploadedFile.objects.all()
    filter_backends = (DjangoFilterBackend, InBBoxFilter)
    filterset_class = filters.UserUploadFileFilter

    def create(self, request):
        """Creates `UserUploadedFile` and its `UserUploadedFileGeometry`.

        Returns:
            dict: uploaded data with name, created_at, created and updated.
        """
        try:
            user_upload, _ = models.UserUploadedFile.objects.get_or_create(
                name=request.data.get('name'),
                user=request.user,
                is_active=True
            )
        except Exception:
            raise Http404('Could not create file on database')

        created_data = 0
        data_exists = 0

        if not 'geometry' in request.data or \
           not 'features' in request.data['geometry']:
            raise Http404('Could not create file on database')

        for feature in request.data['geometry']['features']:
            try:
                geom = GEOSGeometry(str(feature['geometry']))

                if geom.hasz:
                    geom = GEOSGeometry(WKBWriter(dim=2).write_hex(geom))

                _, created = models.UserUploadedFileGeometry.objects.get_or_create(
                    user_uploaded=user_upload,
                    geom=geom,
                    properties=feature['properties']
                )

                if created:
                    created_data = created_data + 1
                else:
                    data_exists = data_exists + 1
            except Exception:
                raise Http404('Could not create geometries on database')

        data = {
            'name': user_upload.name,
            'created_at': user_upload.date_created,
            'created': created_data,
            'updated': data_exists
        }

        return response.Response(data, status=status.HTTP_201_CREATED)


class UserUploadFileListGeometryView(Auth, generics.ListAPIView):
    """View to retrieve `models.UserUploadedFileGeometry` model data.

    Raises:
        Unauthenticated: User is not authenticated

    Returns:
        dict: uploaded file data.
    """

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


class UserUploadFileListView(
    Auth,
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


class UserUploadFileRetrieveUpdateDestroyView(
    Auth,
    generics.RetrieveUpdateDestroyAPIView
):
    """Class for delete and update User Upload File data."""

    serializer_class = serializers.UserUploadedFileSerializer
    queryset = models.UserUploadedFile.objects.all()
    lookup_field = 'id'


class UserSettingsUpdateView(Auth, generics.UpdateAPIView):
    """View to update authenticated User Settings.

    Parameters:
      dark_mode_active (bool): Theme mode
    """

    serializer_class = serializers.UserSettingsSerializer

    def update(self, request, *args, **kwargs):
        theme_mode = request.data.get('theme_mode')

        partial = kwargs.pop('partial', True)

        instance, created = models.User.objects.update_or_create(
            id=self.request.user.id,
            defaults={'dark_mode_active': theme_mode}
        )

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return response.Response(
            {
                "message": "Configurações atualizadas com sucesso!",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class RegisterView(Public, generics.CreateAPIView):
    """
    Handles registration requests and sends an email with the details.
    """
    serializer_class = AccessRequestSerializer
    queryset = models.AccessRequest.objects.all()

    def perform_create(self, serializer):

        instance = serializer.save()

        self._send_notification_email(instance)

    def _send_notification_email(self, instance):
        subject = 'Pedido de acesso ao CMR'
        template_path = os.path.join(
            settings.EMAIL_TEMPLATES_DIR, 'solicitacao_de_acesso.html')

        html_message = render_to_string(template_path, {'name': instance.name})

        try:
            send_mail(
                subject=subject,
                message='',
                from_email="cmr@funai.gov.br",
                recipient_list=settings.RECIPIENT_LIST_EMAIL_DEV,
                html_message=html_message
            )
        except Exception as e:
            logger.error(f"Erro ao enviar email: {str(e)}")


class UserUploadFileUpdatePropertiesPatchView(Auth, generics.UpdateAPIView):
    serializer_class = serializers.UserUploadedFileGeometryListSerializer
    lookup_field = 'id'

    def get_object(self):
        uploaded_file_id = self.kwargs.get('id')
        if not uploaded_file_id:
            raise NotFound("Id não encontrado na URL.")

        try:
            return models.UserUploadedFileGeometry.objects.get(
                user_uploaded__user=self.request.user,
                id=uploaded_file_id
            )
        except models.UserUploadedFileGeometry.DoesNotExist:
            raise NotFound(
                "Geometria não encontrada ou não pertence ao usuário.")

    def patch(self, request, *args, **kwargs):
        # A ideia de PATCH é justamente atualizar parcialmente o objeto
        uploaded_file = self.get_object()

        color = request.data.get('color')
        name = request.data.get('name')

        # Atualiza properties se foi fornecida cor
        if color is not None:
            properties = uploaded_file.properties or {}
            properties['color'] = color
            uploaded_file.properties = properties

        # Atualiza name se foi fornecido
        if name is not None:
            uploaded_file.name = name

        # Salva alterações
        uploaded_file.save()

        data = {
            'id': uploaded_file.id,
            'properties': uploaded_file.properties,
            'name': uploaded_file.name
        }
        return response.Response(data, status=status.HTTP_200_OK)


class InstitutionListView(Auth, generics.ListAPIView):
    """"API to return all available institutions.

    Returns:
        queryset: institution queryset
    """

    queryset = models.Institution.objects.all()
    serializer_class = serializers.InstitutionSerializer


class RoleRetrieveUpdateDestroyView(
    Auth,
    generics.RetrieveUpdateDestroyAPIView
):
    """Role retrieve, update and destroy view data."""

    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()
    lookup_field = 'id'


class RoleListCreateView(Auth, generics.ListCreateAPIView):
    """Role list and create view data."""

    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()


class GroupRetrieveUpdateDestroyView(
    Auth,
    generics.RetrieveUpdateDestroyAPIView
):
    """Group retrieve, update and destroy view data."""

    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    lookup_field = 'id'


class GroupListCreateView(Auth, generics.ListCreateAPIView):
    """Group list and create view data."""

    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()


# class AccessRequestViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for managing AccessRequest data.

#     - POST /user/access-requests/  -> Public
#     - GET /user/access-requests/   -> AdminAuth
#     - GET /user/access-requests/pending/ -> AdminAuth
#     - POST /user/access-requests/<pk>/approve/ -> AdminAuth
#     """

#     queryset = models.AccessRequest.objects.all()
#     serializer_class = AccessRequestSerializer

#     def get_permissions(self):
#         """
#         Assign different permission classes based on action.
#         """
#         if self.action == 'create':
#             # A solicitação de acesso (POST) deve ser pública
#             permission_classes = [Public]
#         elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy', 'list_pending', 'approve']:
#             # Todas as outras ações exigem AdminAuth
#             permission_classes = [AdminAuth]
#         else:
#             permission_classes = [AdminAuth]

#         return [permission() for permission in permission_classes]

#     @action(detail=False, methods=['get'], url_path='pending')
#     def list_pending(self, request):
#         """
#         Lists only requests where status=False (still pending).
#         Accessible only by admin (AdminAuth).
#         """
#         pending_requests = self.queryset.filter(status=False)
#         serializer = self.get_serializer(pending_requests, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @action(detail=True, methods=['post'], url_path='approve')
#     def approve(self, request, pk=None):
#         """
#         Approves a specific access request, marking status=True
#         and recording dt_approvement. Accessible only by admin.
#         """
#         try:
#             access_request = models.AccessRequest.objects.get(
#                 pk=pk, status=False)
#         except models.AccessRequest.DoesNotExist:
#             return Response(
#                 {'detail': 'Requisição não encontrada ou já aprovada.'},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         access_request.status = True
#         access_request.dt_approvement = timezone.now()
#         access_request.save()

#         return Response(
#             {
#                 'detail': 'Acesso aprovado com sucesso.',
#                 'request_id': access_request.id
#             },
#             status=status.HTTP_200_OK
#         )

class AccessRequestListCreateView(Public, generics.ListCreateAPIView):
    """
    Handles creation of new access requests (Public).
    """

    queryset = models.AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer


class AccessRequestPendingView(Public, generics.ListCreateAPIView):
    """
    Lists only pending access requests (AdminAuth).
    """
    queryset = models.AccessRequest.objects.filter(status=False)
    serializer_class = AccessRequestSerializer


class AccessRequestApproveView(Public, APIView):
    """
    Approves a specific access request by marking status=True and
    updating dt_approvement (AdminAuth).
    """

    def post(self, request, pk, *args, **kwargs):

        access_request = get_object_or_404(
            models.AccessRequest,
            pk=pk,
            status=False
        )

        access_request.status = True
        access_request.dt_approvement = timezone.now()
        access_request.save()

        return Response(
            {
                "detail": "Acesso aprovado com sucesso.",
                "request_id": access_request.id,
            },
            status=status.HTTP_200_OK,
        )


class AccessRequestDetailView(Public, generics.RetrieveAPIView):
    """
    Retrieves details of a specific access request (AdminAuth).
    """
    queryset = models.AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer
