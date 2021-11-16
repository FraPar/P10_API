"""api_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import debug_toolbar
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from rest_framework import routers

from authenticate.views import UserRegistrationView, UserLoginView
from api.views import ProjectViewSet, ContributorViewSet, IssueViewSet,CommentViewSet

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'users', ContributorViewSet, basename='contributors')
router.register(r'issues', IssueViewSet, basename='issues')
router.register(r'comments', CommentViewSet, basename='comments')
# re_path(r'^projects/(?P<pk>[0-9]+)/$', UserProjectViewSet, basename='user_projects'),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('authenticate/', include('authenticate.urls')),
    path('signup/', UserRegistrationView.as_view(), name="signup"),
    path('signin/', UserLoginView.as_view(), name="signin"),
    path('', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]