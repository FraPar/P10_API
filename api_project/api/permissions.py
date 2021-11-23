from rest_framework import permissions
from api.models import Contributors, Projects


class AuthorOrAdmin(permissions.BasePermission):

    queryset = Projects.objects.all()

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        project_id = request.path.split('/')[2]
        this_project = self.queryset.filter(project_id=project_id)

        if request.user.is_superuser:
            return True

        if request.user == this_project[0].author_user:
            return True

        return False


class IsAuthor(permissions.BasePermission):

    queryset = Projects.objects.all()

    def has_permission(self, request, view):
        project_id = request.path.split('/')[2]
        this_project = self.queryset.filter(project_id=project_id)
        if request.user.is_superuser:
            return True
        if request.user == this_project[0].author_user:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        this_project = self.queryset.filter(project_id=obj.project_id)
        if request.user.is_superuser:
            return True
        try:
            if obj.author_user == request.user:
                return True
        except AttributeError:
            if this_project[0].author_user == request.user:
                return True
        return False
        

class IsContributor (permissions.BasePermission):

    projectset = Projects.objects.all()
    contributorset = Contributors.objects.all()

    def has_permission(self, request, view):
        project_id = request.path.split('/')[2]
        this_project = self.contributorset.filter(project_id=project_id)
        for data in this_project:
            if request.user == data.user:
                return True


    def has_object_permission(self, request, view, obj):
        project_id = request.path.split('/')[2]
        this_project = self.contributorset.filter(project_id=project_id)
        for data in this_project:
            if data.user == request.user:
                return True
        return False
