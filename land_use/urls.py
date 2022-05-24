from django.urls import path

from land_use import views


urlpatterns = [
    path(
        '',
        views.LandUseView.as_view(),
        name='mapping'
    ),
    path(
        'detail/<int:id>/',
        views.LandUseDetailView.as_view(),
        name='mapped-detail'
    ),
    path(
        'years/',
        views.LandUseYearsView.as_view(),
        name='mapped-years'
    ),
    path(
        'classes/',
        views.LandUseClassesView.as_view(),
        name='mapped-classes'
    ),
    path(
        'table/',
        views.LandUseTableView.as_view(),
        name='mapped-table'
    ),
    path(
        'stats/',
        views.LandUseStatsView.as_view(),
        name='mapped-stats'
    )
]
