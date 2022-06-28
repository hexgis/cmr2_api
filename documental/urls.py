from django.urls import path

from documental import views

urlpatterns = [
    path(
        'list-actions/',
        views.ActionListView.as_view(),
        name='listar-action'
    ),
    path(
        'list/',
        views.DocumentalListViews.as_view(),
        name='list-doc'
    )
]