from django.urls import path
from .views import LayerPermissionListView, ComponentPermissionListView

urlpatterns = [
    path(
        'layer/',
        LayerPermissionListView.as_view(),
        name='layer-permissions'
    ),
    path(
        'component/',
        ComponentPermissionListView.as_view(),
        name='component-permissions'
    ),
]
