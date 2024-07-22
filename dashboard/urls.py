from django.urls import path

from dashboard import views

urlpatterns = [
    path(
        'get-all/',
        views.FindAllDashboardDataView.as_view(),
        name='dashboard_data'
    ),
]
