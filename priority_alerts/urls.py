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
        'detail/',
        views.AlertsDetailView.as_view(),
        name='alerts-detail'
    ),
    path(
        'stats/',
        views.AlertsStatsView.as_view(),
        name='alerts-stats'
    ),
    path(
        'classes/',
        views.AlertsClassesView.as_view(),
        name='alerts-classes'
    ),
]
