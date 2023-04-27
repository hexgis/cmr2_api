from rest_framework import (
    views,
    response
)

from authorization import constant


class LoggedUserPermissions(views.APIView):
    """Logged in user permissions."""

    def get(self, request, *args, **kwargs):
        """Lists all permissions associated to the logged in user."""
        return response.Response(request.user.get_all_permissions())


class LoggedUserModulosCMR(views.APIView):
    """Logged in user access."""

    def get(self, request, *args, **kwargs):
        """Informs which 'ModulosCMR' the logged in user has access to."""
        perms_moduloscmr = dict()

        for moduloscmr in list(constant.MODULOS_CMR.keys()):
            perms_moduloscmr.update({moduloscmr: request.user.has_perms(constant.MODULOS_CMR[moduloscmr]["access"])})

        return response.Response(perms_moduloscmr)