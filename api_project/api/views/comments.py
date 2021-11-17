from django.db.models import query
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.serializers import CommentSerializer
from api.models import Comments


class CommentViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = CommentSerializer 

    def post(self, request, pk):

        serializer = self.serializer_class(data=request.data)
        # print("serializer")
        # print(serializer)
        # print("pk")
        # print(pk)
        # print("request.user")
        # print(request.user)
        # print(request.user.id)

        serializer.is_valid(raise_exception=True)

        serializer.save(author_user=request.user)
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Comment registered successfully',
            }
        
        return Response(response, status=status_code)

    def get_queryset(self):
        issue_id = self.request.path.split('/')[2]
        queryset = Comments.objects.filter(issue_id=issue_id)
        for comments in queryset:
            print(comments.issue_id)
            print(comments.description)
        return queryset

    def update(self, request, *args, **kwargs):
        queryset = Comments.objects.all()
        project_id = self.request.path.split('/')[2]
        queryset = queryset.filter(comment_id=request.data["comment_id"])
        print(queryset)
        if queryset.exists():
            data = request.data
            print("data")
            print(data)
            queryset.update(description=data["description"])
        
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                'message': 'Comment updated successfully',
                }
        else:
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'False',
                'status code' : status_code,
                'message': 'Comment not founded1',
                }
        
        return Response(response, status=status_code)

    def destroy(self, request, *args, **kwargs):
        queryset = Comments.objects.all()

        comment_id = self.request.path.split('/')[2]
        queryset = queryset.filter(comment_id=comment_id)
        print(queryset)
        if queryset.exists():
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                'message': 'Comment deleted successfully',
                }

        else:
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'False',
                'status code' : status_code,
                'message': 'Comment not founded1',
                }

        return Response(response, status=status_code)
        