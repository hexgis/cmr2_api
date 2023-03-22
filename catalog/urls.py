from django.urls import path
from django.conf.urls import url
from catalog import views


urlpatterns = [
    path('satellite/',
        views.SatelliteView.as_view(),
        name='satellite-catalog'
     ),
    path('',
         views.CatalogsView.as_view(),
         name='catalog-scenes'
    ),
    path('',
         views.SatelliteDetailView.as_view(),
         name='detail/'
    ),
    url('first/', views.firstFunc),
    path('sat/',
        views.SatelliteXView.as_view(),
        name='lsa-one'
     ),
]
