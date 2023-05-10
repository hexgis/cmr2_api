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


class LoggedUserCMRModules(views.APIView):
    """Logged in user access."""

    def get(self, request, *args, **kwargs):
        """Informs which 'CMR2 Modules' the logged in user has access to."""
        perms_cmrmodules = dict()

        for cmrmodules in list(constant.CMR_MODULES.keys()):
            perms_cmrmodules.update({cmrmodules: request.user.has_perms(constant.CMR_MODULES[cmrmodules]["access"])})

        return response.Response(perms_cmrmodules)