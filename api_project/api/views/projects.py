from django.db.models import query
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework import viewsets
from api.permissions import AuthorOrAdmin, IsAuthor, IsContributor

from api.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from authenticate.models import User
from api.models import Comments, Contributors, Issues, Projects

class ProjectViewSet(
        CreateModelMixin, 
        RetrieveModelMixin, 
        UpdateModelMixin,
        DestroyModelMixin,
        ListModelMixin,
        viewsets.GenericViewSet
    ):

    permission_classes = [IsAuthenticated,AuthorOrAdmin]
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):

        user_profile = User.objects.get(id=request.user.id)
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        print(user_profile.id)
        serializer.save(author_user_id=user_profile.id)
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Project registered successfully',
            }
        
        return Response(response, status=status_code)

    def get_queryset(self):
        queryset = Projects.objects.filter(author_user=self.request.user)
        try:
            project_id = self.request.path.split('/')[2]
            if project_id is not None:
                queryset = queryset.filter(project_id=project_id)
        except:
            pass

        return queryset
