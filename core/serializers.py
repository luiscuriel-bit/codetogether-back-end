from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Collaborator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

        
class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaborator
        fields = '__all__'

    def validate(self, data):
        project_id = data.get('project_id')
        user_id = data.get('user_id')

        if Collaborator.objects.filter(project_id=project_id, user_id=user_id).exists():
            raise serializers.ValidationError('This user is already a collaborator for this project.')

        return data