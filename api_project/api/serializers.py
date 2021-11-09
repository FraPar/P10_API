from rest_framework import serializers
from .models import Projects
from .models import User


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ('author_user_id', 'project_id', 'title', 'description', 'type')
