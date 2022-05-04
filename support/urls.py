from django.urls import path

from support import views

urlpatterns = [
    path('layers-groups/<int:id>/', views.LayersGroupView.as_view(),
         name='layers-groups'),

    path('categorys-groups/', views.CategoryLayersGroupView.as_view(),
         name='Category-layer-groups'
         )
]
