from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from portal import views

urlpatterns = [
    path('video', views.VideoView.as_view(), name='video-cmr'),
    path('contato', views.ContactView.as_view() ,name='contato'),
    path('cadastro', views.RegisterView.as_view() ,name='cadastro'),
]
