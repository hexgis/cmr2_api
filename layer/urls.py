from django.urls import path

from layer import views

urlpatterns = [
    # Group
    path(
        'layers-groups/',
        views.GroupsCreateListView.as_view(),
        name='layers-groups'
    ),
    path(
        '<int:id>/layers-groups/',
        views.GroupsUpdateDeleteView.as_view(),
        name='layers-groups'
    ),
    path(
        '',
        views.LayerListView.as_view(),
        name='layers'
    ),
    # Management Instrument
    path(
        'management-instrument/',
        views.InstrumentListCreateView.as_view(),
        name='management-instrument-create-list'
    ),
    path(
        'management-instrument/<int:co_funai>/',
        views.InstrumentRetrieveUpdateDestroyView.as_view(),
        name='management-instrument-detail'
    ),
]
