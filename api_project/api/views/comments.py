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
from authenticate.models import User

from api.serializers import CommentSerializer
from api.models import Comments


class CommentViewSet(
        CreateModelMixin, 
        RetrieveModelMixin, 
        UpdateModelMixin,
        DestroyModelMixin,
        ListModelMixin,
        viewsets.GenericViewSet
    ):

    queryset = Comments.objects.all()

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        issues_pk = self.kwargs["issues_pk"]
        print(issues_pk)
        queryset = Comments.objects.filter(issue_id=issues_pk)
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
        user_id = request.user.id
        print("user_id")
        user_instance = User.objects.filter(id=user_id).first()
        print(user_instance)
        issues_pk = self.kwargs["issues_pk"]
        print(issues_pk)
        print(user_id)
        serializer.is_valid(raise_exception=True)

        serializer.save(author_user=user_instance, issue_id_id = issues_pk)
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Comment registered successfully',
            }
        
        return Response(response, status=status_code)
