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
        views.TiByNameView.as_view(),
        name='busca-ti-por-nome'
    ),
    path(
        'instrumento-gestao/',
        views.BuscaInstrumentoGestaoView.as_view(),
        name='busca-instrumento-gestao'
    )
]
