from django.urls import path

from priority_alerts import views


urlpatterns = [
    path(
        '',
        views.AlertsView.as_view(),
        name='alerts'
    ),
    path(
        'table/',
        views.AlertsTableView.as_view(),
        name='alerts-table'
    ),
    path(
        'detail/<int:id>/',
        views.AlertsDetailView.as_view(),
        name='alerts-detail'
    ),
    path(
        'stats/',
        views.AlertsMapStatsView.as_view(),
        name='alerts-map-stats'
    ),
    path(
        'classes/',
        views.AlertsClassesView.as_view(),
        name='alerts-classes'
    ),
]
