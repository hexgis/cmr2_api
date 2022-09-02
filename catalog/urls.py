from urllib.request import url2pathname
from django.urls import path

from catalog import views

urlpatterns = [
    path('satellite',
         views.SatteliteView.as_view(),
         name='Satellite-catalog'
         ),
    path('',
         views.CatalogView.as_view(),
         name='catalog'
         )
]
