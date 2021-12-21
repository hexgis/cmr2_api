# from .views import XptoView
from django.urls.resolvers import URLPattern

from django.urls import path, include


from priority_monitoring.views import PriorityConsolidatedView
from rest_framework import routers

route = routers.DefaultRouter()
route.register('xptozzz', PriorityConsolidatedView, basename = 'XPTOZZZ')

urlpatterns = [
    # path('xpto1', views.xindex1, name='xindex1'),
    # path('xpto2', views.xindex2, name='xindex2'),
    # path('valor_json', views.valor_json, name='printando JSON'),
    path('xptoz', include(route.urls))
]