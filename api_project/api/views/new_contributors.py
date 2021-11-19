from django.db.models import query
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

from api.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from authenticate.models import User
from api.models import Comments, Contributors, Issues, Projects


class ContributorMixin:
    @action(detail=True, methods=["get", "post", "delete"])
    def users(self, request, pk=None):
        project = self.get_object()
        #project = self.get_all()
        #project = self.get_single()

        class ContributorViewSet(ModelViewSet):

            permission_classes = (IsAuthenticated,)
            authentication_class = JSONWebTokenAuthentication
            serializer_class = ContributorSerializer
            queryset = project.contributors_set.all()

        if request.method == "GET":
            print("get")
            viewset = ContributorViewSet(request=request, format_kwarg=format)
            return viewset.list(request)

        if request.method == "POST":
            print("post")
            data = request.data
            print(data)
            print(data["user_id"])
            print(data["project_id"])
            print(data["permission"])
            print(data["role"])
            viewset = ContributorViewSet(request=request, format_kwarg=format)
            return viewset.list(request)

        if request.method == "DELETE" and pk is not None:
            print("delete")
            print(pk)
            viewset = ContributorViewSet(request=request, format_kwarg=format)
            return viewset.list(request)

