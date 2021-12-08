from django.urls import path

from .views import ChangePassword


urlpatterns = [
    path('change-password', ChangePassword.as_view(),
         name='change-password'),
]
