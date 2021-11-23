from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework import viewsets
from api.permissions import AuthorOrAdmin

from api.serializers import ProjectSerializer
from authenticate.models import User
from api.models import Projects

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
