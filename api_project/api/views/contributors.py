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
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.decorators import action

from api.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from authenticate.models import User
from api.models import Comments, Contributors, Issues, Projects


class ContributorViewSet(
        CreateModelMixin, 
        RetrieveModelMixin, 
        UpdateModelMixin,
        ListModelMixin,
        DestroyModelMixin,
        viewsets.GenericViewSet
    ):

    queryset = Contributors.objects.all()

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ContributorSerializer

    def list(self, request, *args, **kwargs):
        project_pk = self.kwargs["projects_pk"]
        queryset = Contributors.objects.filter(project_id=project_pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user_id = request.data["user_id"]
        project_pk = self.kwargs["projects_pk"]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project_id=project_pk, user_id=user_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self,*args,**kwargs):
        # print("DELETE1")
        project_pk = self.kwargs["projects_pk"]
        user_id = self.get_object().pk
        # print(project_pk)
        # print(user_id)
        # instance = self.get_object()
        # print(instance)
        # self.perform_destroy(instance)
        # print(Contributors.objects.filter(id=user_id))
        Contributors.objects.filter(id=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
