from rest_framework import serializers
from .models import Projects


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ('project_id', 'title', 'description', 'type')
