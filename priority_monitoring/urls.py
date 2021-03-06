from django.urls import path

from priority_monitoring import views


urlpatterns = [
    path(
        'consolidated/',
        views.PriorityConsolidatedView.as_view(),
        name='priority-consolidated'
    ),
    path(
        'consolidated/priorities/',
        views.PrioritiesDistinctedListView.as_view(),
        name='priority-consolidated'
    ),
    path(
        'consolidated/detail/<int:pk>/',
        views.PriorityConsolidatedDetailView.as_view(),
        name='priority-consolidated-detail'
    ),
    path(
        'consolidated/total/',
        views.PriorityConsolidatedStatsView.as_view(),
        name='priority-consolidated-stats'
    ),
    path(
        'consolidated/table/',
        views.PriorityConsolidatedTableView.as_view(),
        name='priority-consolidated-table'
    ),
]
