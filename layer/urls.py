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
    path('', views.LayerListView.as_view(), name='layers')
]
