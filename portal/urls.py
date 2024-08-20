from django.urls import path

from portal import views

urlpatterns = [
    path('video', views.VideoPortalView.as_view(), name='video-cmr'),
    path('contato', views.ContatoView.as_view() ,name='contato')
]
