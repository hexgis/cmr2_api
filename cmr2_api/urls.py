"""
URL configuration for cmr2_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('adm-panel/', include(
        ('admin_panel.urls', 'adm-panel'),
        namespace='adm panel'),
    ),
    path('history/', include(
        ('history.urls', 'history'),
        namespace='history')
    ),
    path('auth/', include(
        ('auth_jwt.urls', 'auth'),
        namespace='auth')
    ),
    path('layer/', include(
        ('layer.urls', 'layer'),
        namespace='layer')
    ),
    path('land-use/', include(
        ('land_use.urls', 'land_use'),
        namespace='land-use')
    ),
    path('user/', include(
        ('user.urls', 'user'),
        namespace='user-profile')
    ),
    path('portal/', include(
        ('portal.urls', 'portal'),
        namespace='portal')
    ),
    path('funai/', include(
        ('funai.urls', 'funai'),
        namespace='funai')
    ),
    path('alerts/', include(
        ('priority_alerts.urls', 'alerts'),
        namespace='alerts'),
    ),
    path('monitoring/consolidated/', include(
        ('monitoring.urls', 'monitoring'),
        namespace='monitoring')
    ),
    path('permission/', include(
        ('permission.urls', 'permission'),
        namespace='permission')
    ),
    path('dashboard/', include(
        ('dashboard.urls', 'dashboard'),
        namespace='dashboard')
    ),

] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
