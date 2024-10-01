from django.urls import path

from auth_jwt import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
     path('obtain_token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('obtain_token/', jwt_views.TokenObtainPairView.as_view(),
#          name='token_obtain_pair'),
    path('refresh_token/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('password-reset/', views.ResetPassword.as_view(), name='password-reset-request'),
    path('confirmar/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),       
]
