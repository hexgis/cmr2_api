from django.urls import path

from documental import views

urlpatterns = [
    path(
        'list-actions/',
        views.ActionListView.as_view(),
        name='listar-action'
    )
]