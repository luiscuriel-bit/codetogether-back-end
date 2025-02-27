from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (CollaboratorViewSet, NotificationViewSet, ProjectViewSet,
                    UserViewSet)

app_name = "core"

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"collaborators", CollaboratorViewSet)
router.register(r"notifications", NotificationViewSet, basename='notification')

urlpatterns = [
    path("", include(router.urls)),
]
