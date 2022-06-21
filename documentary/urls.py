from django.urls import path

from documentary import views

urlpatterns = [
    path(
        'list-actions/',
        views.ActionListVeiw.as_view(),
        name='listar-action'
    )
]
