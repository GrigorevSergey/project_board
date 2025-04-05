from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BoardViewSet, NotificationViewSet, ProjectViewSet, TaskViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"boards", BoardViewSet)
router.register(r"tasks", TaskViewSet)
router.register(r"notifications", NotificationViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
