from django.urls import path

from user_profile import views


urlpatterns = [
     path('logged/',
         views.UserLoggedGetView.as_view(),
         name='logged'),
     path('update-settings/',
         views.UserLoggetUpdateView.as_view(),
         name='update-settings'),
     path('upload-file/',
         views.UserUploadFileCreateView.as_view(),
         name='upload-file-create'),
     path('upload-file/list/',
         views.UserUploadFileListView.as_view(),
         name='upload-file-list'),
     path('upload-file/<int:id>/delete/',
         views.UserUploadFileDelete.as_view(),
         name='upload-file-delete'),
     path('upload-file/<int:id>/update/',
         views.UserUploadFileUpdate.as_view(),
         name='upload-file-update'),
     path('upload-file/geo/<int:id>/',
         views.UserUploadFileListGeometryView.as_view(),
         name='upload-file-geometry'),
     path('upload-file/geo/detail/<int:id>/',
         views.UserUploadFileGeometryDetailView.as_view(),
         name='upload-file-geometry-detail'),
     path('give-user-permissions/',
         views.GiverUserPermission.as_view(),
         name='give-user-permissions'),
]
