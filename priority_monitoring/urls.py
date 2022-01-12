from django.urls import path

from priority_monitoring import views


urlpatterns = [
    path(
        'consolidated/',
        views.PriorityConsolidatedView.as_view(),
        name='priority-consolidated'
    ),
    path(
        'consolidated/detail/<int:pk>',
        views.PriorityConsolidatedDetailView.as_view(),
        name='priority-consolidated-detail'
    ),
]
