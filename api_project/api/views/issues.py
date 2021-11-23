from django.db.models import query
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from api.permissions import AuthorOrAdmin, IsAuthor, IsContributor

from api.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from authenticate.models import User
from api.models import Comments, Contributors, Issues, Projects


class IssueViewSet(
        CreateModelMixin, 
        RetrieveModelMixin, 
        UpdateModelMixin,
        DestroyModelMixin,
        ListModelMixin,
        viewsets.GenericViewSet
    ):

    queryset = Issues.objects.all()

    permission_classes = [IsAuthenticated, IsContributor]
    authentication_class = JSONWebTokenAuthentication
    serializer_class = IssueSerializer 

    def list(self, request, *args, **kwargs):
        project_pk = self.kwargs["projects_pk"]
        queryset = Issues.objects.filter(project_id=project_pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        # print("serializer")
        # print(serializer)
        # print("pk")
        # print(pk)
        user_id = request.data["assignee_user_id"]
        user_instance = User.objects.filter(id=user_id).first()
        print(user_instance)
        project_pk = self.kwargs["projects_pk"]
        print(user_id)
        serializer.is_valid(raise_exception=True)

        serializer.save(project_id=project_pk, assignee_user_id=user_instance)
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Issue registered successfully',
            }
        
        return Response(response, status=status_code)
