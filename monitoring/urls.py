from django.urls import path

from monitoring import views


urlpatterns = [
    path(
        '',
        views.MonitoringConsolidatedView.as_view(),
        name='monitoring'
    ),
    path(
        'detail/<int:id>/',
        views.MonitoringConsolidatedDetailView.as_view(),
        name='monitoring-detail'
    ),
    path(
        'map-stats/',
        views.MonitoringConsolidatedMapStatsView.as_view(),
        name='monitoring-map-stats'
    ),
    path(
        'classes/',
        views.MonitoringConsolidatedClassesView.as_view(),
        name='monitoring-classes'
    ),
    path(
        'table/',
        views.MonitoringConsolidatedTableView.as_view(),
        name='monitoring-table'
    ),
    path(
        'table-stats/',
        views.MonitoringConsolidatedTableStatsView.as_view(),
        name='monitoring-table-stats'
    ),
    path(
        'table-stats2/',
        views.MonitoringConsolidatedTableStatsView2.as_view(),
        name='monitoring-table-stats'
    )
]
