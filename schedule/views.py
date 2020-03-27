from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers

from .serializers import *

import logging

logger = logging.getLogger(__name__)


class LessonViewSet(viewsets.ViewSet):
    def transform_result(self, data):
        result = {'monday': list(), 'tuesday': list(), 'wednesday': list(), 'thursday': list(),
                  'friday': list(), 'saturday': list(), 'sunday': list()}
        for i in data:
            logger.error(i.day_of_week)
            if i.day_of_week == 1:
                result['monday'].append(LessonSerializer(i).data)
            if i.day_of_week == 2:
                result['tuesday'].append(LessonSerializer(i).data)
            if i.day_of_week == 3:
                result['wednesday'].append(LessonSerializer(i).data)
            if i.day_of_week == 4:
                result['thursday'].append(LessonSerializer(i).data)
            if i.day_of_week == 5:
                result['friday'].append(LessonSerializer(i).data)
            if i.day_of_week == 6:
                result['saturday'].append(LessonSerializer(i).data)
            if i.day_of_week == 7:
                result['sunday'].append(LessonSerializer(i).data)
        return result

    def list(self, request):
        queryset = Lesson.objects.all()
        serializer = LessonSerializer(queryset, many=True)
        return Response({'lessons': serializer.data})

    def retrieve(self, request, pk=None):
        queryset = Lesson.objects.filter(group__name=pk)
        # lesson = get_object_or_404(queryset, pk=pk)
        serializer = GroupLessonSerializer(queryset, many=True)

        return Response(self.transform_result(serializer.data))


# class GroupViewSet(APIView):
#     def get(self, request):
#         groups = Groups.objects.all()
#         serializer = GroupSerializer(groups, many=True)
#         return Response({"groups": serializer.data})


class GroupViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Groups.objects.all()
        serializer = GroupSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Groups.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(group)

        return Response(serializer.data)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


from collections import namedtuple

Search = namedtuple('Search', ('groups', 'teachers', 'classrooms'))


class SearchViewSet(viewsets.ViewSet):
    """
    Search for groups, teachers and classrooms.
    """

    def list(self, request):
        search = Search(
            groups=Groups.objects.all(),
            teachers=Teacher.objects.all(),
            classrooms=Classroom.objects.all(),
        )
        serializer = SearchSerializer(search)
        return Response(serializer.data)


class JSONGroupsView(APIView):
    def get(self, request):
        import urllib.request, json

        with urllib.request.urlopen("https://rasp.dmami.ru/groups-list.json") as url:
            response = json.loads(url.read().decode())

        return Response(response)
