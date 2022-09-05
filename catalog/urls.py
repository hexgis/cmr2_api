from urllib.request import url2pathname
from django.urls import path

from catalog import views

urlpatterns = [
    path('satellite',
         views.SatelliteView.as_view(),
         name='Satellite-catalog'
     ),
    
]