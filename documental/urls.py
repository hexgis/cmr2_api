# from django.urls import path

# from documental import views

# from django.conf.urls.static import static
# from django.conf import settings


from django.urls import path, include
from rest_framework import routers
from documental import views
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()

urlpatterns = router.urls


urlpatterns = [
    path(
        'list-actions/',
        views.ActionListView.as_view(),
        name='list-actions'
    ),
    path(
        'list/',
        views.DocumentalListViews.as_view(),
        name='list-doc'
    ),
    # path(
    #     'upload/',
    #     views.DocumentUploadView.as_view(),
    #     name='upload-doc'
    # ),
    path(
        'upload6',
        views.UploadTest6view.as_view(),
        name='upload-6'
    ),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
