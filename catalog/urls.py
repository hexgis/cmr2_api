from django.urls import path

from catalog import views

urlpatterns = [
    path('sattelite',
        views.SatteliteView.as_view(),
        name='sattelite-catalog'
    ),
    path('',
         views.CatalogView.as_view(),
         name='catalog'
     )
]
