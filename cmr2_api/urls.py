"""cmr2_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="CMR API",
        default_version='v1',
        description="CMR Api service",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="cmr@funai.gov.br"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(
    #    permissions.IsAuthenticated, permissions.IsAdminUser
    # ),
)


urlpatterns = [
    path('api/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('api-docs/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('admin/', admin.site.urls),
    path('auth/', include(
        ('auth_jwt.urls', 'auth'), namespace='auth')
    ),
    path('support/', include(
        ('support.urls', 'support'), namespace='support')
    ),
    path('priority/', include(
        ('priority_monitoring.urls', 'priority_monitoring'),
        namespace='priority')
    ),
    path('funai/', include(
        ('funai.urls', 'funai'),
        namespace='funai')
    ),
    path('monitoring/', include(
        ('monitoring.urls', 'monitoring'),
        namespace='monitoring')
    ),
    path('alerts/', include(
        ('priority_alerts.urls', 'alerts'),
        namespace='alerts'),
    ),
    path('land-use/', include(
        ('land_use.urls', 'land-use'),
        namespace='land-use'),
    ),
    path('documentary/', include(
        ('documentary.urls','documentary'),
        namespace='documentary'),
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
