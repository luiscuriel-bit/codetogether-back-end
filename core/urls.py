from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProjectViewSet, CollaboratorViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'collaborators', CollaboratorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]