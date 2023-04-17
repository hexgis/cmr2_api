from rest_framework.decorators import api_view

from rest_framework import response


@api_view()
def logged_user_permissions(request):
    """Lists all permissions associated to the logged in user."""
    return response.Response(request.user.get_all_permissions())
