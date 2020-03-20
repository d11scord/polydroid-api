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
            logger.error(i.day)
            if i.day == 'monday':
                result['monday'].append(LessonSerializer(i).data)
            if i.day == 'tuesday':
                result['tuesday'].append(LessonSerializer(i).data)
            if i.day == 'wednesday':
                result['wednesday'].append(LessonSerializer(i).data)
            if i.day == 'thursday':
                result['thursday'].append(LessonSerializer(i).data)
            if i.day == 'friday':
                result['friday'].append(LessonSerializer(i).data)
            if i.day == 'saturday':
                result['saturday'].append(LessonSerializer(i).data)
            if i.day == 'sunday':
                result['sunday'].append(LessonSerializer(i).data)
        return result

    def list(self, request):
        queryset = Lesson.objects.all()
        serializer = LessonSerializer(queryset, many=True)
        return Response({'lessons': serializer.data})

    def retrieve(self, request, pk=None):
        queryset = Lesson.objects.filter(group__title=pk)
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


class AuditoryViewSet(viewsets.ModelViewSet):
    queryset = Auditory.objects.all()
    serializer_class = AuditorySerializer


# class SearchViewSet(APIView):
#     def get(self, request):
#         groups_queryset = Groups.objects.all()
#         teachers_queryset = Teacher.objects.all()
#         classroms_queryset = Auditory.objects.all()
#         all_objects = list(groups_queryset) + list(teachers_queryset) + list(classroms_queryset)
#         response = serializers.serialize('json', all_objects)
#         return Response(response)


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
            classrooms=Auditory.objects.all(),
        )
        serializer = SearchSerializer(search)
        return Response(serializer.data)


class JSONGroupsView(APIView):
    def get(self, request):
        import urllib.request, json

        with urllib.request.urlopen("https://rasp.dmami.ru/groups-list.json") as url:
            response = json.loads(url.read().decode())

        return Response(response)
