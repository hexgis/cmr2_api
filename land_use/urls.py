from django.urls import path

from land_use import views


urlpatterns = [
    path(
        'consolidated/',
        views.LandUseView.as_view(),
        name=''
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
        'detail/',
        views.LandUseDetailView.as_view(),
        name='mapped-detail'
    ),
    path(
        'table/',
        views.LandUseTableView.as_view(),
        name='mapped-table'
    ),
    path(
        'states/',
        views.LandUseStatesView.as_view(),
        name='mapped-states'
    )
]
