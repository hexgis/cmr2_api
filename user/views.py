from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.contrib.gis.geos.error import GEOSException
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.exceptions import ValidationError
from user import models, serializers
from rest_framework import generics, status
from . import models
from user.models import User, Role
from django.shortcuts import get_object_or_404
from rest_framework import status
from smtplib import SMTPException
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
from rest_framework.exceptions import NotFound

from rest_framework_gis.filters import InBBoxFilter
from .serializers import AccessRequestSerializer, AccessRequestDetailSerializer
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
from django.http import FileResponse, JsonResponse, Http404


from user import (
    serializers,
    models,
    filters
)
from permission import models as perm_models

from utils.send_email import send_custom_email

logger = logging.getLogger(__name__)


class UserListView(Auth, generics.ListCreateAPIView):
    """"API to return all users along with their respective sector ID.

    Returns:
        queryset: user and sector_id queryset
    """

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a user.

    Supported methods:
    - GET: Returns the details of a specific user based on their ID.
    - PATCH: Partially updates an existing user's data.
    - PUT: Fully updates an existing user's data.
    - DELETE: Removes the user from the database or optionally deactivates them.

    URL Parameters:
    - pk (int): ID of the user to be managed.
    """

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(
            {"message": "Usuário desativado com sucesso."},
            status=status.HTTP_204_NO_CONTENT
        )


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
    """View para listar e criar arquivos enviados pelo usuário."""

    serializer_class = serializers.UserUploadedFileSerializer
    queryset = models.UserUploadedFile.objects.all()
    filter_backends = (DjangoFilterBackend, InBBoxFilter)
    filterset_class = filters.UserUploadFileFilter

    def create(self, request):
        """
        Creates UserUploadedFile and its associated geometries.

        Args:
            request: HTTP request containing the upload data

        Returns:
            Response: Upload data with name, creation date and count of items created/updated

        Raises:
            ValidationError: If the input data is invalid
            Http404: If a serious error occurs during processing
        """
        if not request.data.get('name'):
            raise ValidationError('O campo "name" é obrigatório')

        if 'geometry' not in request.data or 'features' not in request.data.get('geometry', {}):
            raise ValidationError('Estrutura de geometria inválida ou ausente')

        try:
            with transaction.atomic():
                user_upload, _ = models.UserUploadedFile.objects.get_or_create(
                    name=request.data['name'],
                    user=request.user,
                )

                created_data = 0
                data_exists = 0

                for feature in request.data['geometry']['features']:
                    try:
                        if 'geometry' not in feature:
                            continue
                        geom = GEOSGeometry(str(feature['geometry']))

                        if geom.hasz:
                            from django.contrib.gis.geos import WKBWriter
                            geom = GEOSGeometry(
                                WKBWriter(dim=2).write_hex(geom))

                        _, created = models.UserUploadedFileGeometry.objects.get_or_create(
                            user_uploaded=user_upload,
                            geom=geom,
                            properties=request.data.get('properties', {})
                        )

                        if created:
                            created_data += 1
                        else:
                            data_exists += 1

                    except GEOSException as e:
                        raise ValidationError(f'Erro na geometria: {str(e)}')
                    except Exception as e:
                        raise ValidationError(
                            f'Erro ao processar feature: {str(e)}')

                response_data = {
                    'name': user_upload.name,
                    'created_at': user_upload.date_created,
                    'created': created_data,
                    'updated': data_exists
                }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Erro ao criar upload: {str(e)}')
            raise Http404(f'Erro ao processar o upload: {str(e)}')


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
            user=self.request.user.id
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


class InstitutionListCreateView(Auth, generics.ListCreateAPIView):
    """API para listar e criar instituições."""

    queryset = models.Institution.objects.all()
    serializer_class = serializers.InstitutionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstitutionRetrieveUpdateDestroyView(Auth, APIView):
    """API para recuperar, atualizar e excluir uma instituição."""

    def get_object(self, pk):
        return get_object_or_404(models.Institution, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        institution = self.get_object(pk)
        serializer = serializers.InstitutionSerializer(institution)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        institution = self.get_object(pk)
        serializer = serializers.InstitutionSerializer(
            institution, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        institution = self.get_object(pk)
        serializer = serializers.InstitutionSerializer(
            institution, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        institution = self.get_object(pk)
        institution.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class RoleDiffView(Public, APIView):
    """ Returns the difference between the groups associated with a role and the groups not associated with it. """

    def get(self, request, id=None):
        try:
            role = get_object_or_404(models.Role, id=id)
            unassociated_groups = models.Group.objects.exclude(
                id__in=role.groups.values_list('id', flat=True))
            group_serializer = serializers.GroupSerializer(
                unassociated_groups, many=True)

            return Response(
                {
                    "unassociated_groups": group_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "error": "An unexpected error occurred.",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GroupRetrieveUpdateDestroyView(
    Public,
    generics.RetrieveUpdateDestroyAPIView
):
    """Group retrieve, update and destroy view data."""

    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    lookup_field = 'id'


class GroupListCreateView(Public, generics.ListCreateAPIView):
    """Group list and create view data."""

    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()


class GroupDiffListView(Public, APIView):
    """ Returns the difference between the permissions associated with a group and the permissions not associated with it. """

    def get(self, request, group_id):
        group = get_object_or_404(models.Group, id=group_id)

        unassociated_layer_permissions = perm_models.LayerPermission.objects.exclude(
            groups=group)

        unassociated_component_permissions = perm_models.ComponentPermission.objects.exclude(
            groups=group)

        data = {
            "layer_permissions": [
                {"id": permission.id, "name": permission.name,
                    "description": permission.description}
                for permission in unassociated_layer_permissions
            ],
            "component_permissions": [
                {"id": permission.id, "name": permission.name,
                    "description": permission.description}
                for permission in unassociated_component_permissions
            ]
        }

        return Response(data, status=status.HTTP_200_OK)


class AccessRequestListCreateView(Public, generics.ListCreateAPIView):
    """
    Handles creation of new access requests (Public).
    """

    queryset = models.AccessRequest.objects.all()
    serializer_class = AccessRequestDetailSerializer


class AccessRequestPendingView(Public, generics.ListCreateAPIView):
    """
    Lists only pending access requests (AdminAuth).
    """
    queryset = models.AccessRequest.objects.filter(status=1)
    serializer_class = AccessRequestSerializer


class AccessRequestApproveView(AdminAuth, APIView):
    """
    Approves a specific access request,
    updating dt_approvement, and creating a User entry if one does not exist.
    Also sends a notification email upon approval.
    """

    def post(self, request, pk, *args, **kwargs):
        try:
            admin = request.user

            permissions = request.data.get('permissions', {})
            institution_id = permissions.get('selected_group')
            role_ids = permissions.get('selected_roles', [])

            access_request = get_object_or_404(
                models.AccessRequest,
                pk=pk,
                status=models.AccessRequest.StatusType.PENDENTE
            )

            institution = get_object_or_404(
                models.Institution, pk=institution_id)
            roles = models.Role.objects.filter(pk__in=role_ids)
            access_request.status = 2
            access_request.reviewed_at = timezone.now()
            access_request.reviewed_by = admin
            access_request.save()

            user, created = User.objects.get_or_create(
                email=access_request.email,
                defaults={
                    'username': access_request.email,
                    'first_name': access_request.name,
                    'institution': institution,
                }
            )

            if created:
                user.roles.set(roles)
                user.save()
                logger.info(f"Usuário criado: {user.email}, acesso aprovado")

                subject = 'Pedido de acesso aprovado'
                recipients = [access_request.email,
                              'valdean.junior@hex360.com.br']
                template_path = os.path.join(
                    settings.EMAIL_TEMPLATES_DIR,
                    'approvedUser.html'
                )
                context = {
                    'user_name': access_request.name
                }
                email_sent = send_custom_email(
                    subject=subject,
                    recipients=recipients,
                    template_path=template_path,
                    context=context,
                )
                if email_sent:
                    return Response({'detail': 'E-mail enviado com sucesso.'}, status=200)
                else:
                    return Response({'detail': 'Falha ao enviar o e-mail.'}, status=500)

            else:
                logger.info(f"Usuário '{user.email}' já existia na base.")

        except Http404:
            return Response(
                {'detail': 'Requisição não encontrada ou já aprovada.'},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return Response(
                {'detail': 'Erro inesperado durante a aprovação.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "detail": "Acesso aprovado e usuário cadastrado com sucesso.",
                "request_id": access_request.id,
                "user_id": user.id
            },
            status=status.HTTP_200_OK
        )


class AccessRequestDetailView(Public, generics.RetrieveAPIView):
    """
    Retrieves details of a specific AccessRequest with formatted and related data.
    """
    queryset = models.AccessRequest.objects.all()
    serializer_class = AccessRequestDetailSerializer


class AccessRequestRejectView(AdminAuth, generics.RetrieveAPIView):

    def patch(self, request, pk, *args, **kwargs):
        try:
            deined_details = request.data.get('denied_details')
            access_request = get_object_or_404(
                models.AccessRequest,
                pk=pk,
                status=models.AccessRequest.StatusType.PENDENTE
            )

            access_request.status = 3
            access_request.reviewed_at = timezone.now()
            access_request.reviewed_by = request.user
            access_request.denied_details = deined_details

            access_request.save()

            return Response(
                {
                    "detail": "Acesso negado ao usuário.",
                    "request_id": access_request.id,
                    "user_id": request.user.id
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return Response(
                {'detail': 'Erro inesperado durante a aprovação.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomLoginView(LoginView):
    template_name = 'admin/login.html'  # usa o template bonito do Jazzmin
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/priority_api/admin_app/'  # redirecionamento fixo
