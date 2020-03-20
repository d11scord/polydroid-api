"""Polydroid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from rest_framework import routers
from django.contrib import admin
from django.urls import path, include

from schedule.views import *

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'lessons-list', LessonViewSet, basename='lessons')
router.register(r'teachers-list', TeacherViewSet)
router.register(r'classrooms-list', AuditoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # url(r'^groups/$', GroupViewSet.as_view()),
    url(r'^search/$', SearchViewSet.as_view({'get': 'list'})),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
