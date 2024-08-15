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
    path('send-email-test/', views.SendEmailTest.as_view(), name='send email test'),
    path('get-permissons-test/', views.RequestPermissions.as_view(), name='get permissions test'),
    path('grant-permissions-test/', views.GrantPermissions.as_view(), name='grant permissions test'),
    path('revoke-permission/', views.RevokePermissions.as_view(), name='revoke permissions test'),
    path('test/', views.CreatePermissionsView.as_view(), name='test'),
]
