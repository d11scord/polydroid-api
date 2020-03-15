from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class AuditoryViewSet(viewsets.ModelViewSet):
    queryset = Auditory.objects.all()
    serializer_class = AuditorySerializer


class JSONGroupsView(APIView):
    def get(self, request):
        import urllib.request, json

        with urllib.request.urlopen("https://rasp.dmami.ru/groups-list.json") as url:
            response = json.loads(url.read().decode())

        return Response(response)
