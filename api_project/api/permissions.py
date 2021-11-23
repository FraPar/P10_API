from rest_framework import permissions
from api.models import Comments, Contributors, Issues, Projects


class AuthorOrAdmin(permissions.BasePermission):

    queryset = Projects.objects.all()

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            print("Is Authenticated")
            return True

    def has_object_permission(self, request, view, obj):
        project_id = request.path.split('/')[2]
        this_project = self.queryset.filter(project_id=project_id)

        if request.user.is_superuser:
            print("Is Authenticated as superuser")
            return True

        if request.user == this_project[0].author_user:
            print("Is Authenticated as author")
            return True

        return False


class IsAuthor(permissions.BasePermission):

    queryset = Projects.objects.all()

    def has_permission(self, request, view):
        project_id = request.path.split('/')[2]
        this_project = self.queryset.filter(project_id=project_id)
        if request.user.is_superuser:
            print("Is Authenticated as superuser")
            return True
        if request.user == this_project[0].author_user:
            print("Is Authenticated as author")
            return True
        return False

    def has_object_permission(self, request, view, obj):
        this_project = self.queryset.filter(project_id=obj.project_id)
        if request.user.is_superuser:
            print("Is Authenticated as superuser")
            return True
        try:
            if obj.author_user == request.user:
                print("Is Authenticated as Author")
                return True
        except AttributeError:
            print(this_project[0].author_user)
            print(request.user)
            if this_project[0].author_user == request.user:
                print("Is Authenticated as Author")
                return True
        return False
        

class IsContributor (permissions.BasePermission):

    projectset = Projects.objects.all()
    contributorset = Contributors.objects.all()

    def has_permission(self, request, view):
        project_id = request.path.split('/')[2]
        this_project = self.contributorset.filter(project_id=project_id)
        print("this_project")
        print(this_project)
        for data in this_project:
            print("data.user")
            print(data.user)
            print("request.user")
            print(request.user)
            if request.user == data.user:
                print("Is Contributor")
                return True


    def has_object_permission(self, request, view, obj):
        project_id = request.path.split('/')[2]
        this_project = self.contributorset.filter(project_id=project_id)
        print("this_project")
        print(this_project)
        for data in this_project:
            print("data.user")
            print(data.user)
            print("request.user")
            print(request.user)
            if data.user == request.user:
                print("Is Contributor")
                return True
            print(data.project)
        print(request)
        print(request)
        return False
