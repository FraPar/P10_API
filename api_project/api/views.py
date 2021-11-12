from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import ProjectSerializer
from authenticate.models import User
from .models import Projects


class ProjectViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ProjectSerializer

    def post(self, request):

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
        queryset = Projects.objects.all()
        print("project")
        for project in queryset:
            print(project.project_id)
        try:
            project_id = self.request.path.split('/')[2]
            if project_id is not None:
                queryset = queryset.filter(project_id=project_id)
        except:
            pass

        return queryset

    def update(self, request, *args, **kwargs):
        queryset = Projects.objects.all()
        try:
            project_id = self.request.path.split('/')[2]
            queryset = queryset.filter(project_id=project_id)
            if queryset.exists():
                data = request.data
                queryset.update(title=data["title"], description=data["description"], type=data["type"])
            
                status_code = status.HTTP_201_CREATED
                response = {
                    'success' : 'True',
                    'status code' : status_code,
                    'message': 'Project updated successfully',
                    }
            else:
                status_code = status.HTTP_201_CREATED
                response = {
                    'success' : 'False',
                    'status code' : status_code,
                    'message': 'Project not founded',
                    }
        
        except:
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'False',
                'status code' : status_code,
                'message': 'Project not founded',
                }

        return Response(response, status=status_code)

    def destroy(self, request, *args, **kwargs):
        queryset = Projects.objects.all()
        try:
            project_id = self.request.path.split('/')[2]
            queryset = queryset.filter(project_id=project_id)
            if queryset.exists():
                queryset.delete()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success' : 'True',
                    'status code' : status_code,
                    'message': 'Project deleted successfully',
                    }

            else:
                status_code = status.HTTP_201_CREATED
                response = {
                    'success' : 'False',
                    'status code' : status_code,
                    'message': 'Project not founded',
                    }
        except:
            status_code = status.HTTP_201_CREATED

            response = {
                'success' : 'False',
                'status code' : status_code,
                'message': 'Project not founded',
                }

        return Response(response, status=status_code)
        
