from django.urls import path

from user_profile import views


urlpatterns = [
    path('logged/',
         views.UserLoggedGetView.as_view(),
         name='logged'),
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
]
