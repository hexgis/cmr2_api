from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from portal import views

urlpatterns = [
    path('video', views.VideoPortalView.as_view(), name='video-cmr'),
    path('contato', views.ContatoView.as_view() ,name='contato'),
    path('cadastro', views.CadastroView.as_view() ,name='cadastro'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)