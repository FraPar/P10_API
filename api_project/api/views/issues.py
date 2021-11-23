from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from api.permissions import IsContributor

from api.serializers import IssueSerializer
from authenticate.models import User
from api.models import Issues


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
        user_id = request.data["assignee_user_id"]
        user_instance = User.objects.filter(id=user_id).first()
        project_pk = self.kwargs["projects_pk"]
        serializer.is_valid(raise_exception=True)

        serializer.save(project_id=project_pk, author_user=user_instance)
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Issue registered successfully',
            }
        
        return Response(response, status=status_code)

    def destroy(self, request, *args, **kwargs):
        issue_id = request.path.split('/')[-2]
        issueset = Issues.objects.filter(issue_id=issue_id)
        if issueset.exists():
            if issueset[0].author_user_id == request.user.id:
                return super().destroy(request, *args, **kwargs)
            return Response({"Status":"Vous n'êtes pas l'auteur du problème"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"Status":"Pas de problème trouvé"},status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        issue_id = request.path.split('/')[-2]
        issueset = Issues.objects.filter(issue_id=issue_id)
        if issueset.exists():
            if issueset[0].author_user_id == request.user.id:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
            return Response({"Status":"Vous n'êtes pas l'auteur du problème"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"Status":"Pas de problème trouvé"},status=status.HTTP_400_BAD_REQUEST)
    