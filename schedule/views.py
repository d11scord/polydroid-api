from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

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
#         response = {
#             'groups': groups_queryset.data,
#             'teachers': teachers_queryset.data,
#             'classrooms': classroms_queryset.data,
#         }
#         return Response(response)


class JSONGroupsView(APIView):
    def get(self, request):
        import urllib.request, json

        with urllib.request.urlopen("https://rasp.dmami.ru/groups-list.json") as url:
            response = json.loads(url.read().decode())

        return Response(response)
