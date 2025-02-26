from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    code = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Collaborator(models.Model):
    ROLE_CHOICES = [("admin", "Admin"), ("editor", "Editor"), ("viewer", "Viewer")]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="collaborations"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="collaborators"
    )
    role = models.CharField(max_length=6, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "project"], name="unique_collaborator"
            )
        ]

    def __str__(self):
        return self.role


class Notification(models.Model):
    STATUS_CHOICES = [("unread", "Unread"), ("read", "Read")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default="unread")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}..."
