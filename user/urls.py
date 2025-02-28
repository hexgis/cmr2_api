from django.urls import path, include

from user import views


urlpatterns = [
    path('', views.UserListView.as_view(), name='user-list'),
    path('logged/', views.UserLoggedGetView.as_view(), name='logged'),
    path('update-settings/', views.UserSettingsUpdateView.as_view(),
         name='update-settings'),
    path(
        'upload-file/', views.UserUploadFileListCreateView.as_view(),
        name='upload-file'
    ),
    path(
        'upload-file/list/',
        views.UserUploadFileListView.as_view(),
        name='upload-file-list'
    ),
    path(
        'upload-file/geo/<int:id>/',
        views.UserUploadFileListGeometryView.as_view(),
        name='upload-file-geometry'
    ),
    path(
        'upload-file/geo/detail/<int:id>/',
        views.UserUploadFileGeometryDetailView.as_view(),
        name='upload-file-geometry-detail'
    ),
    path(
        'upload-file/<int:id>/',
        views.UserUploadFileRetrieveUpdateDestroyView.as_view(),
        name='upload-delete-file'
    ),
    path(
        'register/',
        views.RegisterView.as_view(),
        name='register'
    ),
    path(
        'upload-file/geo/<int:id>/update-properties/',
        views.UserUploadFileUpdatePropertiesPatchView.as_view(),
        name='upload-properties'
    ),
    path(
        'institution/',
        views.InstitutionListView.as_view(),
        name='institution'
    ),
    path(
        'role/',
        views.RoleListCreateView.as_view(),
        name='role-list'
    ),
    path(
        'role/<int:id>/',
        views.RoleRetrieveUpdateDestroyView.as_view(),
        name='role'
    ),
    path(
        'role-diff/<int:id>/',
        views.RoleDiffView.as_view(),
        name='role-difference-list'
    ),
    path(
        'group/',
        views.GroupListCreateView.as_view(),
        name='group-list'
    ),
    path(
        'group/<int:id>/',
        views.GroupRetrieveUpdateDestroyView.as_view(),
        name='group'
    ),
    path(
        'group-diff/<int:group_id>/',
        views.GroupDiffListView.as_view(),
        name='group-diff'
    ),
    path(
        'access-requests/',
        views.AccessRequestListCreateView.as_view(),
        name='access-request-create'
    ),
    path(
        'access-requests/pending/',
        views.AccessRequestPendingView.as_view(),
        name='access-request-pending'
    ),
    path(
        'access-requests/<int:pk>/approve/',
        views.AccessRequestApproveView.as_view(),
        name='access-request-approve'
    ),
    path(
        'access-requests/<int:pk>/reject/',
        views.AccessRequestRejectView.as_view(),
        name='access-request-reject'
    ),
    path(
        'access-requests/<int:pk>/',
        views.AccessRequestDetailView.as_view(),
        name='access-request-detail'
    ),
]
