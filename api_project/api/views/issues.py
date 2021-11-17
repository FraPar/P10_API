from django.db.models import query
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from authenticate.models import User
from api.models import Comments, Contributors, Issues, Projects


class IssueViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = IssueSerializer 

    def post(self, request, pk):

        serializer = self.serializer_class(data=request.data)
        # print("serializer")
        # print(serializer)
        # print("pk")
        # print(pk)

        serializer.is_valid(raise_exception=True)

        serializer.save(project_id=pk)
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Project registered successfully',
            }
        
        return Response(response, status=status_code)

    def get_queryset(self):
        project_id = self.request.path.split('/')[2]
        queryset = Issues.objects.filter(project=project_id)
        for issues in queryset:
            # print(contribs)
            # print(contribs.project)
            # print(contribs.project_id)
            print(issues.project)
            print(issues.title)
            print(issues.issue_id)
            # print(contribs.permission)
        return queryset

    def update(self, request, *args, **kwargs):
        queryset = Issues.objects.all()
        try:
            project_id = self.request.path.split('/')[2]
            queryset = queryset.filter(issue_id=request.data["issue_id"])
            if queryset.exists():
                data = request.data
                queryset.update(title=data["title"], desc=data["desc"], tag=data["tag"], priority=data["priority"], status=data["status"])
            
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
        queryset = Issues.objects.all()
        try:
            project_id = self.request.path.split('/')[2]
            queryset = queryset.filter(project_id=project_id,issue_id=request.data["issue_id"])
            if queryset.exists():
                queryset.delete()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success' : 'True',
                    'status code' : status_code,
                    'message': 'Issue deleted successfully',
                    }

            else:
                status_code = status.HTTP_201_CREATED
                response = {
                    'success' : 'False',
                    'status code' : status_code,
                    'message': 'Issue not founded',
                    }
        except:
            status_code = status.HTTP_201_CREATED

            response = {
                'success' : 'False',
                'status code' : status_code,
                'message': 'Issue not founded',
                }

        return Response(response, status=status_code)
    