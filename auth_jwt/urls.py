from django.urls import path

from auth_jwt import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('obtain_token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('refresh_token/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('change-password/',
         views.ChangePassword.as_view(),
         name='change-password'),
]
