from django.urls import path

from dashboard import views

urlpatterns = [
    path(
        'get-all/',
        views.FindAllDashboardDataView.as_view(),
        name='dashboard_data'
    ),
    path(
        'download-csv/',
        views.GenCSV.as_view(),
        name='dashboard_data'
    ),
]
