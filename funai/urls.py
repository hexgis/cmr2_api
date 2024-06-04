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
    path(
        'busca-geo-ti/',
        views.BuscaGeoTIListView.as_view(),
        name='busca-geo-ti-list'
    ),
    path(
        'ti-by-name/',
        views.TiByName.as_view(),
        name='busca-ti-por-nome'
    )
]
