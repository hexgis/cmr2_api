from django.urls import resolve
from rest_framework.permissions import AllowAny

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
            'cadastro',
        ]

        if route_name in open_routes:
            request._disable_jwt = True

        response = self.get_response(request)
        return response