from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Collaborator, Notification, Project
from .serializers import (CollaboratorSerializer, NotificationSerializer,
                          ProjectSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                email=serializer.validated_data.get("email", ""),
                password=serializer.validated_data["password"],
                first_name=serializer.validated_data.get("first_name", ""),
                last_name=serializer.validated_data.get("last_name", ""),
            )
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    **UserSerializer(user).data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def notifications(self, request, pk=None):
        notifications = Notification.objects.filter(user=pk)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(collaborators__user=user)
   
    @action(detail=True, methods=["GET"])
    def collaborators(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        collaborators = project.collaborators.all()
        serializer = CollaboratorSerializer(collaborators, many=True)
        return Response(serializer.data)



class CollaboratorViewSet(viewsets.ModelViewSet):
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def add_collaborator(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)

        username = request.data.get("user")
        user = get_object_or_404(User, username=username)
        role = request.data.get("role", "viewer")

        collaborator, created = Collaborator.objects.get_or_create(
            project=project, user=user, defaults={"role": role}
        )

        if created:
            return Response(
                {"message": f"{user.username} has been added as a collaborator."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "The user is already a collaborator."}, status=status.HTTP_400_BAD_REQUEST,
            )


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
