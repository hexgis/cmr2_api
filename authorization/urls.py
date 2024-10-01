from django.urls import path
from authorization import views


urlpatterns = [
    path(
        'user_permissions/',
        views.LoggedUserPermissions.as_view(),
        name='authorization-user-permissions'
    ),
    path(
        'user_cmrmodules/',
        views.LoggedUserCMRModules.as_view(),
        name='authorization-user-cmrmodules'
    ),
    path('create-permissions/', views.CreatePermissionsView.as_view(), name='Create Permissions'),
]
