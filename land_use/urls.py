from django.urls import path

from land_use import views


urlpatterns = [
    path(
        '',
        views.LandUseView.as_view(),
        name='mapping'
    ),
    path(
        'detail/<int:id>/',
        views.LandUseDetailView.as_view(),
        name='mapped-detail'
    ),
    path('stats/', views.LandUseStatsView.as_view(),name='mapped-stats'),
    path('table/', views.LandUseTabletView.as_view(), name='table-land-use'),
    path('search/', views.LandUsePerTiSearchListView.as_view(), name='search-land-use'),

]
