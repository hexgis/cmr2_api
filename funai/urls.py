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
    ),
    path(
        'village-by-name/',
        views.IndegenousVillageByNameView.as_view(),
        name='teste2'
    ),
    path(
        'ti-study-by-name/',
        views.TiInStudyByName.as_view(),
        name='teste3'
    )
]
