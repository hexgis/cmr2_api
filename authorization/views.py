from django.shortcuts import render

# Create your views here.

from rest_framework import (
    permissions,
    generics,
    response,
    status
)
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required, login_required


class AuthModelMixIn:
    """Default Authentication for `deter_monitoring` views."""
    permission_classes = (permissions.IsAuthenticated,)


class AuthorizationUserPermissions(AuthModelMixIn, generics.RetrieveAPIView):
    pass



@api_view()
def firstFunc(request):
    return response.Response(request.user.get_all_permissions())


