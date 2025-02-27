from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Collaborator, Notification, Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
            instance.save()

        return super().update(instance, validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def create(self, validated_data):
        owner = validated_data.pop("owner")
        project = Project.objects.create(owner=owner, **validated_data)

        Collaborator.objects.create(user=owner, project=project, role="admin")
        Notification.objects.create(user=owner, message=f"You created the project '{project.name}'.")
        
        return project


class CollaboratorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Collaborator
        fields = "__all__"

    def validate(self, data):
        project = data.get("project")
        user = data.get("user")

        if Collaborator.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError(
                "This user is already a collaborator for this project."
            )

        return data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
