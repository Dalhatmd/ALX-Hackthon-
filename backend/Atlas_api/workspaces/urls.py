from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkspaceViewSet, AmenityViewSet, WorkspaceTypeViewSet

router = DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet)
router.register(r'amenities', AmenityViewSet)
router.register(r'workspace-types', WorkspaceTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
