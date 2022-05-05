from django.urls import path

from land_use import views


urlpatterns = [
    path(
        'consolidated/',
        views.LandUseMappingView.as_view(),
        name=''
    ),
    path(
        'years/',
        views.LandUseMappingYearsView.as_view(),
        name='mapped-years'
    ),
    path(
        'classes/',
        views.LandUseMappingClassesView.as_view(),
        name='mapped-classes'
    ),
    path(
        'detail/',
        views.LandUseMappingDetailView.as_view(),
        name='mapped-detail'
    ),
    path(
        'table/',
        views.LandUseMappingTableView.as_view(),
        name='mapped-table'
    ),
    path(
        'states/',
        views.LandUseMappingStatesView.as_view(),
        name='mapped-states'
    )
]
