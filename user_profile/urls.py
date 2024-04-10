from django.urls import path

from user_profile import views


urlpatterns = [
    path('logged/',
         views.UserLoggedGetView.as_view(),
         name='logged'),
    path('upload-file/list/',
         views.UserUploadFileListView.as_view(),
         name='upload-file-list'),
]
