from django.db.models import query
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from authenticate.models import User
from api.models import Comments, Contributors, Issues, Projects


class ContributorViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ContributorSerializer

    def get(self, request, *args, **kwargs):
        users = Contributors.objects.all()
        serializer = ContributorSerializer(users, many=True)
        print(request)
        print(request.data)
        print(request.user)
        print(request.user.id)

        return Response(serializer.data)

    def create(self, request, pk):
        print("post pk")
        print(pk)
        print("data=request.data")
        print(request.data)

        user_profile = User.objects.get(id=request.data["user_id"])
        project_profile = Projects.objects.get(project_id=request.data["project_id"])

        all_contributor = Contributors.objects.all()
        print("all_contributor")
        print(all_contributor)
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=user_profile, project=project_profile)
        
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Contributor added successfully',
            }
        
        return Response(response, status=status_code)

    def destroy(self, request, *args, **kwargs):
        queryset = Contributors.objects.all()
        try:
            project_id = self.request.path.split('/')[2]
            queryset = queryset.filter(project=project_id,user=request.data["user_id"])
            if queryset.exists():
                queryset.delete()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success' : 'True',
                    'status code' : status_code,
                    'message': 'Contributor deleted successfully',
                    }

            else:
                status_code = status.HTTP_201_CREATED
                response = {
                    'success' : 'False',
                    'status code' : status_code,
                    'message': 'Contributor not founded',
                    }
        except:
            status_code = status.HTTP_201_CREATED

            response = {
                'success' : 'False',
                'status code' : status_code,
                'message': 'Contributor not founded',
                }

        return Response(response, status=status_code)

