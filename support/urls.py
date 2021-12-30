from django.urls import path

from support import views

urlpatterns = [
    path('layers-groups/', views.LayersGroupView.as_view(),
         name='layers-groups'),
]
