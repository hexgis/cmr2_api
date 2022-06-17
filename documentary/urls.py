from django import views
from django.urls import path

from documentary import views

urlpatterns = [
    path(
        'list-actions/',
        views.AcaoListVeiw.as_view(),
        name='listar-acao'
    ),
]

