from collections import namedtuple

import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

logger = logging.getLogger(__name__)


class ScheduleGroup(viewsets.ViewSet):
    def transform_result(self, data):
        """
        Метод для трансформации данных расписания одной группы.
        Распределяет данные по дням недели, а в них по номеру пары.
        :param data: Данные для трансформации.
        :return: трансформированный для отображения dict.
        """
        # Делаем заготовку по дням недели и количеству пар,
        # чтобы повторить структуру оригинальный JSON.
        result = {
            'monday'   : dict({i: list() for i in range(1, 8)}),
            'tuesday'  : dict({i: list() for i in range(1, 8)}),
            'wednesday': dict({i: list() for i in range(1, 8)}),
            'thursday' : dict({i: list() for i in range(1, 8)}),
            'friday'   : dict({i: list() for i in range(1, 8)}),
            'saturday' : dict({i: list() for i in range(1, 8)}),
            'sunday'   : dict({i: list() for i in range(1, 8)}),
        }
        for i in data:
            # logger.error(i.number)
            if i.day_of_week == 1:
                result['monday'][i.number].append(LessonSerializer(i).data)
            if i.day_of_week == 2:
                result['tuesday'][i.number].append(LessonSerializer(i).data)
            if i.day_of_week == 3:
                result['wednesday'][i.number].append(LessonSerializer(i).data)
            if i.day_of_week == 4:
                result['thursday'][i.number].append(LessonSerializer(i).data)
            if i.day_of_week == 5:
                result['friday'][i.number].append(LessonSerializer(i).data)
            if i.day_of_week == 6:
                result['saturday'][i.number].append(LessonSerializer(i).data)
            if i.day_of_week == 7:
                result['sunday'][i.number].append(LessonSerializer(i).data)
        return result

    def list(self, request):
        """
        Получаем список всех пар.
        """
        queryset = Lesson.objects.all()
        serializer = LessonSerializer(queryset, many=True)
        return Response({'lessons': serializer.data})

    @action(detail=True)
    def retrieve_lesson(self, request, id=None):
        """
        Получаем детальную информацию об одной паре.
        :param id: первичный ключ пары.
        """
        queryset = Lesson.objects.all()
        lesson = get_object_or_404(queryset, pk=id)
        serializer = LessonSerializer(lesson)

        return Response(serializer.data)

    def retrieve_group(self, request, id=None):
        """
        Получаем расписание на неделю для группы.
        :param id: первичный ключ группы.
        :return: трансформированный для отображения JSON.
        """
        queryset = Lesson.objects.filter(group__id=id)
        serializer = ScheduleGroupSerializer(queryset, many=True)

        return Response(self.transform_result(serializer.data))

    def retrieve_teacher(self, request, id=None):
        """
        Получаем расписание на неделю для группы.
        :param id: первичный ключ группы.
        :return: трансформированный для отображения JSON.
        """
        queryset = Lesson.objects.filter(teachers__id=id)
        serializer = LessonSerializer(queryset, many=True)

        return Response(serializer.data)


class GroupViewSet(viewsets.ViewSet):
    """
    Вьюсет для списка и детализации групп.
    """
    def list(self, request):
        """
        Метод для получения списка групп.
        :return: JSON-список всех групп.
        """
        queryset = Groups.objects.all()
        serializer = GroupSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Детализация информации по конкреной группе.
        :param pk: первичный ключ группы.
        :return: JSON-объект с информацией о группе.
        """
        queryset = Groups.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(group)

        return Response(serializer.data)


class TeacherViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для списка и детализации преподавателей.
    Методы для этих действий реализуются автоматически.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для списка и детализации аудиторий.
    Методы для этих действий реализуются автоматически.
    """
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


Search = namedtuple('Search', ('groups', 'teachers', 'classrooms'))


class SearchViewSet(viewsets.ViewSet):
    """
    Вьюсет для поиска групп, преподавателей и аудиторий без детализации.
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
    """
    Вью для загрузки списка групп.
    """
    def get(self, request):
        import urllib.request
        import json

        with urllib.request.urlopen("https://rasp.dmami.ru/groups-list.json") as url:
            response = json.loads(url.read().decode())

        return Response(response)
