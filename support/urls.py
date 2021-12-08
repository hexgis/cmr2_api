from django.urls import path

from .views import LayersGroupView

urlpatterns = [
    path('layers-groups', LayersGroupView.as_view(),
         name='layers-groups'),
]
