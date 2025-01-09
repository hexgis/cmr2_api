from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user import views

router = DefaultRouter()
router.register(
    r'access-requests',
    views.AccessRequestViewSet,
    basename='accessrequest'
)

urlpatterns = [
    path('', views.UserListView.as_view(), name='user-list'),
    path('logged/', views.UserLoggedGetView.as_view(), name='logged'),
    path('update-settings/', views.UserSettingsUpdateView.as_view(),
         name='update-settings'),
    path('upload-file/', views.UserUploadFileListCreateView.as_view(),
         name='upload-file'),
    path('upload-file/list/', views.UserUploadFileListView.as_view(),
         name='upload-file-list'),
    path('upload-file/geo/<int:id>/',
         views.UserUploadFileListGeometryView.as_view(), name='upload-file-geometry'),
    path('upload-file/geo/detail/<int:id>/',
         views.UserUploadFileGeometryDetailView.as_view(), name='upload-file-geometry-detail'),
    path('upload-file/<int:id>/',
         views.UserUploadFileRetrieveUpdateDestroyView.as_view(), name='upload-delete-file'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('upload-file/geo/<int:id>/update-properties/',
         views.UserUploadFileUpdatePropertiesPatchView.as_view(), name='upload-properties'),
    path('institution/', views.InstitutionListView.as_view(), name='institution'),
    path('role/', views.RoleListCreateView.as_view(), name='role-list'),
    path('role/<int:id>/', views.RoleRetrieveUpdateDestroyView.as_view(), name='role'),
    path('group/', views.GroupListCreateView.as_view(), name='group-list'),
    path('group/<int:id>/', views.GroupRetrieveUpdateDestroyView.as_view(), name='group'),

    path('', include(router.urls)),
]
