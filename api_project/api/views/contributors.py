from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from api.permissions import IsAuthor

from api.serializers import ContributorSerializer
from api.models import Contributors


class ContributorViewSet(
        CreateModelMixin, 
        RetrieveModelMixin, 
        UpdateModelMixin,
        ListModelMixin,
        DestroyModelMixin,
        viewsets.GenericViewSet
    ):

    queryset = Contributors.objects.all()

    permission_classes = [IsAuthenticated, IsAuthor]
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
        queryset = Contributors.objects.filter(project_id=project_pk)
        if queryset.exists():
            for data in queryset:
                test_id = data.user_id
                if str(test_id) == str(user_id):
                    return Response({"Status":"Utilisateur déjà présent sur ce projet"},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project_id=project_pk, user_id=user_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
