from django.urls import path

from dashboard import views

urlpatterns = [
    path(
        'get-all/',
        views.FindAllDashboardDataView.as_view(),
        name='dashboard_data'
    ),
    path(
        'get-year/',
        views.FindDashboardDataYearsView.as_view(),
        name='dashboard_data_year'
    ),
    path(
        'download-csv/',
        views.GenCSV.as_view(),
        name='dashboard_data'
    ),
    path(
        'get-user-login/',
        views.FindUserDashboardDataView.as_view(),
        name='user_dashboard_data'
    ),
]
