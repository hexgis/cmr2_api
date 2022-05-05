from django.urls import path

from land_use import views


urlpatterns = [
    path(
        'consolidated/',
        views.LandUseMappingView.as_view(),
        name=''
    ),
    path(
        'consolidated/years/',
        views.LandUseMappingYearsView.as_view(),
        name='mapped-years'
    ),
    path(
        'consolidated/classes/',
        views.LandUseMappingClassesView.as_view(),
        name='mapped-classes'
    ),
    path(
        'consolidated/detail/',
        views.LandUseMappingDetailView.as_view(),
        name='mapped-detail'
    ),
    path(
        'consolidated/table/',
        views.LandUseMappingTableView.as_view(),
        name='mapped-table'
    ),
    path(
        'consolidated/states/',
        views.LandUseMappingStatesView.as_view(),
        name='mapped-states'
    )
]
