from django.db.models import query
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from authenticate.models import User
from api.models import Comments, Contributors, Issues, Projects
from .new_comments import CommentMixin


class IssueMixin:
    @action(detail=True, methods=["get", "post", "put", "delete"])
    def issues(self, request, pk=None):
        project = self.get_object()
        #project = self.get_all()
        #project = self.get_single()

        class IssueViewSet(ModelViewSet):

            # permission_classes = (IsAuthenticated,)
            # authentication_class = JSONWebTokenAuthentication
            serializer_class = IssueSerializer
            queryset = project.issues_set.all()

        if request.method == "GET":
            print("get")
            viewset = IssueViewSet(request=request, format_kwarg=format)
            return viewset.list(request)

        if request.method == "POST":
            print("post")
            data = request.data
            print(data)
            print(data["title"])
            print(data["desc"])
            print(data["tag"])
            print(data["priority"])
            print(data["status"])
            print(data["assignee_user_id"])
            print(pk)
            viewset = IssueViewSet(request=request, format_kwarg=format)
            return viewset.list(request)

        if request.method == "PUT":
            print("put")
            data = request.data
            viewset = IssueViewSet(request=request, format_kwarg=format)
            return viewset.list(request)

        if request.method == "DELETE" and pk is not None:
            print("delete")
            print(pk)
            viewset = IssueViewSet(request=request, format_kwarg=format)
            return viewset.list(request)

