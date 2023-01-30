from django.urls import path

from deter_monitoring import views

urlpatterns = [
    path(
        'detail/<int:pk>/',
        views.DeterTIDetailView.as_view(),
        name='deter-monitoring-detail'
    ),
    path(
        '',
        views.DeterTIView.as_view(),
        name='deter-monitoring-geomety'
    ),
    path(
        'map-stats/',
        views.DeterTIMapStatsView.as_view(),
        name='deter-monitoring-map-stats'
    ),
    path(
        'table/',
        views.DeterTITableView.as_view(),
        name='deter-monitoring-table'
    ),
    path(
        'table-stats/',
        views.DeterTITableStatsView.as_view(),
        name='deter-monitoring-table-stats'
    )
]
