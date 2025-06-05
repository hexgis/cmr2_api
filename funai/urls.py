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
        'all-data-ti-by-name/',
        views.TiByNameAllInfoView.as_view(),
        name='busca-todas-ti-por-nome'
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
    ),
    # Management Instrument
    path(
        'management-instrument/',
        views.InstrumentListCreateView.as_view(),
        name='management-instrument-create-list'
    ),
    path(
        'management-instrument/<int:co_funai>/',
        views.InstrumentRetrieveUpdateDestroyView.as_view(),
        name='management-instrument-detail'
    ),
]
