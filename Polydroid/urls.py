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

# Списки пар, преподавателей, аудиторий и групп.
lessons_list = ScheduleGroup.as_view({
    'get': 'list',
})
groups_list = GroupViewSet.as_view({
    'get': 'list',
})
teachers_list = TeacherViewSet.as_view({
    'get': 'list',
})
classrooms_list = ClassroomViewSet.as_view({
    'get': 'list',
})

# Детализированная информация о парах, преподавателях, аудиториях и группах.
lesson_detail = ScheduleGroup.as_view({
    'get': 'retrieve_lesson',
})

# Расписания одной группы/преподавателя/аудитории.
lesson_group = ScheduleGroup.as_view({
    'get': 'retrieve_group',
})

lesson_teacher = ScheduleGroup.as_view({
    'get': 'retrieve_teacher',
})


urlpatterns = [
    # Списки
    path('lessons/', lessons_list, name='lessons'),
    path('groups/', groups_list, name='groups'),
    path('teachers/', teachers_list, name='teachers'),
    path('classrooms/', classrooms_list, name='classrooms'),

    # Детализированная информация
    path('lessons/<int:id>/', lesson_detail, name='lesson-detail'),

    # Расписания
    path('schedule/group/<int:id>/', lesson_group, name='lesson-group'),
    path('schedule/teacher/<int:id>/', lesson_teacher, name='lesson-teacher'),

    # Поиск
    url(r'^search-objects/$', SearchViewSet.as_view({'get': 'list'})),

    # Администрирование
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]
