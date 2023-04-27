from django.urls import path
from authorization import views


urlpatterns = [
    path(
        'user_permissions/',
        views.LoggedUserPermissions.as_view(),
        name='authorization-user-permissions'
    ),
    path(
        'user_moduloscmr/',
        views.LoggedUserModulosCMR.as_view(),
        name='authorization-user-moduloscmr'
    ),
]
