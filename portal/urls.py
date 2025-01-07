from django.urls import path
from .views import VideoView, ContactView

urlpatterns = [
    path('video/', VideoView.as_view(), name='video'),
    path('contato/', ContactView.as_view(), name='contact'),
]
