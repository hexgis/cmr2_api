from django.urls import path
from django.conf.urls import url
from authorization import views


urlpatterns = [
    path(
        'user_permissions/',
        views.AuthorizationUserPermissions,
        name='authorization-user-permissions'
    ),
    url('first/', views.firstFunc),
]