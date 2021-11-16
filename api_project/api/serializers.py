from rest_framework import serializers
from .models import Projects, Contributors, Issues, Comments


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ('title', 'description', 'type')


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = ('user_id', 'project_id', 'permission', 'role')


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issues
        fields = ('title', 'desc', 'tag', 'priority', 'project_id', 'status', 'assignee_user_id')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('comment_id', 'description', 'author_user_id', 'issue_id')
