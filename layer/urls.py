from django.urls import path

from layer import views

urlpatterns = [
    # Group
    path('layers-groups/',
         views.GroupsCreateListView.as_view(),
         name='layers-groups'
         ),
    path('<int:id>/layers-groups/',
         views.GroupsUpdateDeleteView.as_view(),
         name='layers-groups'
         ),
    path('',
         views.LayerListView.as_view(),
         name='layers'
         ),
    path('<int:id>/image/base64/',
         views.LayerThumbnailImageBase64View.as_view(),
         name='thumbnail-image-base64'),
    path('<int:id>/legend/base64/',
         views.LayerThumbnailImageBase64View.as_view(),
         name='thumbnail-image-base64'),
]
