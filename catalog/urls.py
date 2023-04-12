from django.urls import path

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
]
