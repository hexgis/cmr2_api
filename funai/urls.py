from django.urls import path

from funai import views


urlpatterns = [
    path(
        'cr/',
        views.CoordenacaoRegionalView.as_view(),
        name='coordenacao-regional'
    ),
    path(
        'ti/',
        views.LimiteTerraIndigenaView.as_view(),
        name='terras-indigenas'
    ),
]
