from django.urls import path


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path(
        'change-password/',
        views.ChangePassword.as_view(),
        name='change-password'
    ),
    path(
        'password-reset/',
        views.ResetPassword.as_view(),
        name='reset-password'
    ),
    path('obtain_token/', TokenObtainPairView.as_view(
        serializer_class=views.CustomTokenObtainPairSerializer
    ), name='token_obtain_pair'),
    path(
        'refresh_token/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'confirmar/',
        views.PasswordResetConfirmView.as_view(),
        name='password-reset-confirm'
    ),

]
