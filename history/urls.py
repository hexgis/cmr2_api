from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogEntryViewSet, UserRoleChangeViewSet

router = DefaultRouter()
router.register(r'logs', LogEntryViewSet)
router.register(r'role-changes', UserRoleChangeViewSet,
                basename='role-changes')

urlpatterns = [
    path('', include(router.urls)),
]
