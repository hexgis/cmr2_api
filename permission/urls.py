from django.urls import path
from .views import GroupPermissionListView, RoleGroupDiffView, LayerPermissionListView, ComponentPermissionListView, LayerPermissionView, LayerPermissionDiffView

urlpatterns = [
    path(
        '',
        LayerPermissionListView.as_view(),
        name='permissions'
    ),
    path(
        'layer/',
        LayerPermissionView.as_view(),
        name='layer-permissions'
    ),
    path(
        'role/',
        GroupPermissionListView.as_view(),
        name='layer-permissions'
    ),
    path(
        'layer/<int:pk>/',
        LayerPermissionView.as_view(),
        name='layer-permission-detail'
    ),
    path(
        'layer-diff/<int:pk>/',
        LayerPermissionDiffView.as_view(),
        name='layer-permission-diff'
    ),
    path(
        'role-diff/<int:pk>/',
        RoleGroupDiffView.as_view(),
        name='layer-permission-diff'
    ),
    path(
        'component/',
        ComponentPermissionListView.as_view(),
        name='component-permissions'
    ),
]
