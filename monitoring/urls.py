from django.urls import path

from monitoring import views


urlpatterns = [
    path(
        'consolidated/',
        views.MonitoringConsolidatedView.as_view(),
        name='monitoring'
    ),
    path(
        'consolidated/detail/<int:id>/',
        views.MonitoringConsolidatedDetailView.as_view(),
        name='monitoring-detail'
    ),
    path(
        'consolidated/map-stats/',
        views.MonitoringConsolidatedMapStatsView.as_view(),
        name='monitoring-map-stats'
    ),
    path(
        'consolidated/classes/',
        views.MonitoringConsolidatedClassesView.as_view(),
        name='monitoring-classes'
    ),
    path(
        'consolidated/table/',
        views.MonitoringConsolidatedTableView.as_view(),
        name='monitoring-table'
    ),
    path(
        'consolidated/table-stats/',
        views.MonitoringConsolidatedTableStatsView.as_view(),
        name='monitoring-table-stats'
    )
]
