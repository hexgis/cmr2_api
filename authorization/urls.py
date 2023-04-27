from django.urls import path
from django.conf.urls import url
from authorization import views


urlpatterns = [
    url(
        'user_permissions/',
        views.logged_user_permissions,
        name='authorization-user-permissions'
    ),
]