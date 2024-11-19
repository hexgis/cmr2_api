import json
import os
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from admin_panel import models as adminPanelModel

from django.urls import resolve
from rest_framework.permissions import AllowAny

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _


class GlobalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == '/adm-panel/tickets/':
            response = self.validate_attachments(request)
            if response:
                return response

        response = self.get_response(request)

        if request.path == '/user/give-user-permissions/':
            if 'application/json' in response.get('Content-Type', ''):
                try:
                    data = json.loads(response.content)
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON: {str(e)}")
                    return response

                # Verifica campos necessários
                if all(k in data for k in ("user", "admin", "new_permissions", "old_permissions")):
                    self.handle_permissions_logging(data)
                else:
                    print("Campos obrigatórios ausentes na resposta JSON.")

        return response

    def validate_attachments(self, request):
        attachments = request.FILES.getlist('attachments')
        invalid_attachments = []
        valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']

        for attachment in attachments:
            ext = os.path.splitext(attachment.name)[1]
            if ext.lower() not in valid_extensions:
                invalid_attachments.append(attachment.name)

        if invalid_attachments:
            return JsonResponse(
                {'invalid_files': invalid_attachments},
                status=400
            )

        return None

    def handle_permissions_logging(self, data):
        User = get_user_model()
        new_permissions = data.get("new_permissions", [])
        old_permissions = data.get("old_permissions", [])
        user = data.get("user")
        admin = data.get("admin")

        user_instance = get_object_or_404(User, id=user)
        admin_instance = get_object_or_404(User, id=admin)

        if new_permissions:
            try:
                # Log de mudança de permissões
                adminPanelModel.ChangePermissionsLog.objects.create(
                    admin_id=admin_instance,
                    user_id=user_instance,
                    old_permissions={'old_permissions': old_permissions},
                    new_permissions={'new_permissions': new_permissions}
                )
                print("Log registrado com sucesso!")
            except Exception as e:
                print(f"Erro ao registrar log: {str(e)}")


class DisableJWTOnPublicRoutesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Desabilita a autenticação JWT para rotas definidas como públicas.
        Identifica o nome da rota e, se a rota estiver listada em `open_routes`, 
        define um atributo personalizado `request._disable_jwt` para que as views 
        possam processá-la sem exigir autenticação.

        :param request: Objeto HTTP de solicitação que representa os dados e o contexto da requisição atual
        :return: Retorna a resposta da view, potencialmente modificada por este middleware
        """
        route_name = resolve(request.path_info).url_name

        open_routes = [
            'password-reset-request',
            'password-reset-confirm',
            'video-cmr',
            'contato',
            'access-request',
            'cadastro',
        ]

        if route_name in open_routes:
            request._disable_jwt = True

        response = self.get_response(request)
        return response
