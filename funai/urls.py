#from django.urls.resolvers import URLPattern
from django.urls import path

from funai import views


urlpatterns = [
    path('cr_data/', views.CoordenacaoRegionalView.as_view(),
        name='coordenacao-regional'
    ),
    path('ti_data/', views.LimiteTerraIndigenaView.as_view(),
        name='terras-indigenas'
    ),
    # path('CrTiFunai', views.CrTiFunaiView.as_Views(),
    #     name='cr-ti-funai'
    # ),
]
