from urllib.request import url2pathname
from django.urls import path

from catalog import views

urlpatterns = [
    path('sattelite',
        views.SatteliteView.as_view(),
        name='sattelite-catalog'
    ),
]