from django.urls import path

from priority_alerts import views


urlpartterns = [
    path(
        '/',
        views.AlertsView.as_view(),
        name=''
    ),
    path(
        'table/',
        views.AlertsTableView.as_view(),
        name=''
    ),
    path(
        'detail/',
        views.AlertsDetailView.as_view(),
        name=''
    ),
    path(
        'stats/',
        views.AlertsStatsView.as_view(),
        name=''
    ),
    path(
        'classes/',
        views.AlertsClassesView.as_view(),
        name=''
    ),
]
