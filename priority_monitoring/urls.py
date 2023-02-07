from django.urls import path

from priority_monitoring import views


urlpatterns = [
    path(
        '',
        views.PriorityConsolidatedView.as_view(),
        name='priority-consolidated'
    ),
    path(
        'priorities/',
        views.PrioritiesDistinctedListView.as_view(),
        name='priority-consolidated-priorities'
    ),
    path(
        'detail/<int:pk>/',
        views.PriorityConsolidatedDetailView.as_view(),
        name='priority-consolidated-detail'
    ),
    path(
        'total/',
        views.PriorityConsolidatedMapStatsView.as_view(),
        name='priority-consolidated-stats'
    ),
    path(
        'table/',
        views.PriorityConsolidatedTableView.as_view(),
        name='priority-consolidated-table'
    ),
]
