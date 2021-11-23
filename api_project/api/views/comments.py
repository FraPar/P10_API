from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from authenticate.models import User
from api.permissions import IsContributor

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

    permission_classes = (IsAuthenticated,IsContributor)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        issues_pk = self.kwargs["issues_pk"]
        queryset = Comments.objects.filter(issue_id=issues_pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        user_id = request.user.id
        user_instance = User.objects.filter(id=user_id).first()
        issues_pk = self.kwargs["issues_pk"]
        serializer.is_valid(raise_exception=True)

        serializer.save(author_user=user_instance, issue_id_id = issues_pk)
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Comment registered successfully',
            }
        
        return Response(response, status=status_code)

    def destroy(self, request, *args, **kwargs):
        comment_id = request.path.split('/')[-2]
        commentset = Comments.objects.filter(comment_id=comment_id)
        if commentset.exists():
            if commentset[0].author_user_id == request.user.id:
                return super().destroy(request, *args, **kwargs)
            return Response({"Status":"Vous n'êtes pas l'auteur du commentaire"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"Status":"Pas de commentaire trouvé"},status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        comment_id = request.path.split('/')[-2]
        commentset = Comments.objects.filter(comment_id=comment_id)
        if commentset.exists():
            if commentset[0].author_user_id == request.user.id:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
            return Response({"Status":"Vous n'êtes pas l'auteur du commentaire"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"Status":"Pas de commentaire trouvé"},status=status.HTTP_400_BAD_REQUEST)
