from django.urls import path

from deter_monitoring import views

urlpatterns = [
    path(
        'detail/<int:pk>/',
        views.DeterDetailView.as_view(),
        name='deter-monitoring-detail'
    ),
    path(
        '',
        views.DeterView.as_view(),
        name='deter-monitoring-geomety'
    ),
    path(
        'map-stats/',
        views.DeterMapStatsView.as_view(),
        name='deter-monitoring-map-stats'
    ),
    path(
        'table/',
        views.DeterTableView.as_view(),
        name='deter-monitoring-table'
    ),
    path(
        'table-stats/',
        views.DeterTableStatsView.as_view(),
        name='deter-monitoring-table-stats'
    )
]