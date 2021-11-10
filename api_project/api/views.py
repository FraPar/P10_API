from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import ProjectSerializer
from authenticate.models import User
from .models import Projects
import re


class ProjectViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ProjectSerializer

    def post(self, request):
        print(User.objects.all())
        user_profile = User.objects.get(id=request.user.id)
        print(Projects.objects.all())
        project_all = Projects.objects.all()

        for project in project_all:
            print(project)
            print(project.author_user)
            print(project.author_user_id)
            print(project.project_id)
            print(project.title)
            print(project.description)

        print("user_profile")
        print(user_profile)
        print(user_profile.id)

        serializer = self.serializer_class(data=request.data)

        print("serializer")
        print(serializer)

        serializer.is_valid(raise_exception=True)
        user_all = User.objects.all()

        for user in user_all:
            print(user.id)

        # user_profile = "b19e4df0-caf4-4f43-9298-4082b5ab6ac4"

        print("user_profile.id")
        print(user_profile)
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
        queryset = Projects.objects.all()
        # for projects in queryset:
        #     print("projects-LIST")
        #     print(projects)
        #     print(projects.project_id)
        # category_id = re.findall('\d+', self.request.path)
        try:
            project_id = self.request.path.split('/')[-2]
        # print("project_id")
        # print(project_id)
            if project_id is not None:
                queryset = queryset.filter(project_id=project_id)
        except:
            pass

        return queryset
