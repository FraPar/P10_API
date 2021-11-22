from rest_framework import permissions
from api.models import Comments, Contributors, Issues, Projects


class AuthorAllStaffAllButEditOrReadOnly(permissions.BasePermission):

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
        print("this_project[0]")
        print(this_project[0])
        print(this_project[0].author_user)
        print(request.user)

        if request.user.is_superuser:
            print("Is Authenticated as superuser")
            return True

        if request.user == this_project[0].author_user:
            print("Is Authenticated as author")
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        print("obj")
        print(obj)
        print(obj.user)
        print(obj.user_id)
        print("obj.project_id")
        print(obj.project_id)
        this_project = self.queryset.filter(project_id=obj.project_id)
        print("this_project")
        print(this_project)
        print("this_project[0]")
        print(this_project[0])
        print("this_project[0].author_user")
        print(this_project[0].author_user)
        print(request)
        print("request.user")
        print(request.user)
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
        print("project_id")
        print(project_id)
        this_project = self.contributorset.filter(project_id=project_id)
        print("this_project")
        print(this_project)
        print("request.user")
        print(request.user)
        for data in this_project:
            print("data.user")
            print(data.user)
            if request.user == data.user:
                print("Is Contributor")
                return True


    def has_object_permission(self, request, view, obj):
        #PROCHAIN ENDROIT A BOSSER !
        print(obj)
        print(obj)
        # if obj in self.queryset:
            # print("Inside Queryset")
        print(self.queryset)
        for data in self.queryset:
            print(data)
            print(data.id)
            print(data.user_id)
            print(data.user)
            print(data.project)
        print(request)
        print(request)
        return False
