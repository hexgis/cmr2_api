from django.urls import path

from support import views

urlpatterns = [
    path(
        'layers-groups/',
        views.LayersGroupView.as_view(),
        name='layers-groups'
    ),

    path(
        'categorys-groups/',
        views.CategoryLayersGroupView.as_view(),
        name='Category-layer-groups'
    ),

    path(
        'layers-info/',
        views.LayersInfoView.as_view(),
        name='layer-info'
    ),
    path(
        'ti-detail/<int:pk>/',
        views.TiDetailView.as_view(),
        name='ti-detail'
    ),
    path(
        'ti-by-name/',
        views.TiByNameView.as_view(),
        name='ti-by-name'
    )
]
