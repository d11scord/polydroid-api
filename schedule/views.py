from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers

from .serializers import *


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer


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
    A simple ViewSet for listing the Tweets and Articles in your Timeline.
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
