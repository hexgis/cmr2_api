from django.urls import path
from .views import LayerPermissionListView, ComponentPermissionListView, LayerPermissionView

urlpatterns = [
    path(
        'layer/',
        LayerPermissionView.as_view(),
        name='layer-permissions'
    ),
    path(
        'layer/<int:pk>/',
        LayerPermissionView.as_view(),
        name='layer-permission-detail'
    ),
    path(
        'component/',
        ComponentPermissionListView.as_view(),
        name='component-permissions'
    ),
]
