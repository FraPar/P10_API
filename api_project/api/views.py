from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import ProjectSerializer
from authenticate.models import User
from .models import Projects


class ProjectRegistrationView(CreateAPIView):

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
            print(project.author_user_id)
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

        serializer.save(author_user_id=user_profile)
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Project registered successfully',
            }
        
        return Response(response, status=status_code)