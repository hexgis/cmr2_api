from django.urls import path

from catalog import views


urlpatterns = [
    path('satellite/',
        views.SatelliteView.as_view(),
        name='satellite-catalog'
     ),
    path('',
         views.CatalogView.as_view(),
         name='catalog'
    ),
    path('xpto/',
         views.CatalogView2.as_view(),
         name='catalog'
    ),
]
