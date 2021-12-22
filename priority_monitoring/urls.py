from django.urls.resolvers import URLPattern
from django.urls import path

from priority_monitoring import views


urlpatterns = [
    path('consolidated/',
         views.PriorityConsolidatedView.as_view(),
         name='priority-consolidated'
    )
]
