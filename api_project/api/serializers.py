from rest_framework import serializers
from .models import Projects, Contributors


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ('title', 'description', 'type')


class UserProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = ('user_id', 'project_id', 'permission', 'role')
