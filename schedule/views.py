from collections import namedtuple
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
import logging

from datetime import datetime

logger = logging.getLogger(__name__)


def get_teacher_name(teacher_id):
    teacher_name = Teacher.objects.get(pk=teacher_id).name
    teacher_name_array = Teacher.objects.get(pk=teacher_id).name.split()
    if len(teacher_name_array) == 3:
        title = teacher_name_array[0] + ' ' + teacher_name_array[1][0] + '. ' + teacher_name_array[2][0] + '.'
    else:
        title = teacher_name
    return title


class ScheduleGroup(viewsets.ViewSet):
    @staticmethod
    def transform_result(data):
        """
        Метод для трансформации данных расписания одной группы.
        Распределяет данные по дням недели, а в них по номеру пары.
        :param data: Данные для трансформации.
        :return: трансформированный для отображения dict.
        """
        # Делаем заготовку по дням недели и количеству пар,
        # чтобы повторить структуру оригинальный JSON.
        result = [
            [list() for i in range(7)],  # 'monday'
            [list() for i in range(7)],  # 'tuesday'
            [list() for i in range(7)],  # 'wednesday'
            [list() for i in range(7)],  # 'thursday'
            [list() for i in range(7)],  # 'friday'
            [list() for i in range(7)],  # 'saturday'
            [list() for i in range(7)],  # 'sunday'
        ]
        for lesson in data:
            result[lesson.day_of_week-1][lesson.number-1].append(LessonSerializer(lesson).data)
        return result

    @staticmethod
    def timestamp():
        """
        :return: Текущая дата и время запроса в милисекундах
        """
        now = datetime.now()
        timestamp = int(datetime.timestamp(now)) * 1000
        return timestamp

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

        title = Groups.objects.get(pk=id).name

        return Response({
            'id': id,
            'date': self.timestamp(),
            'type': 'group',
            'title': title,
            'grid': self.transform_result(serializer.data),
        })

    def retrieve_teacher(self, request, id=None):
        """
        Получаем расписание на неделю для преподавателя.
        :param id: первичный ключ преподавателя.
        :return: трансформированный для отображения JSON.
        """
        queryset = Lesson.objects.filter(teachers__id=id)
        serializer = ScheduleGroupSerializer(queryset, many=True)

        return Response({
            'id': id,
            'date': self.timestamp(),
            'type': 'teacher',
            'title': get_teacher_name(id),
            'grid': self.transform_result(serializer.data),
        })



    def retrieve_classroom(self, request, id=None):
        """
        Получаем расписание на неделю для аудитории.
        :param id: первичный ключ аудитории.
        :return: трансформированный для отображения JSON.
        """
        queryset = Lesson.objects.filter(classrooms__id=id)
        serializer = ScheduleGroupSerializer(queryset, many=True)

        title = Classroom.objects.get(pk=id).name

        return Response({
            'id': id,
            'date': self.timestamp(),
            'type': 'classroom',
            'title': title,
            'grid': self.transform_result(serializer.data),
        })

    def retrieve_search(self, request):
        """
        Получаем расписание на неделю по поисковому параметру.
        :return: трансформированный для отображения JSON.
        """
        search_parameter = request.GET.get('q')
        if search_parameter is None or search_parameter == "":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        groups = Groups.objects.filter(name__contains=search_parameter)
        teachers = Teacher.objects.filter(name__contains=search_parameter)
        classrooms = Classroom.objects.filter(name__contains=search_parameter)
        suitable_count = groups.count() + teachers.count() + classrooms.count()
        if suitable_count == 1:
            if groups.count() == 1:
                id = groups.first().id
                type = 'group'
                title = Groups.objects.get(pk=id).name
                queryset = Lesson.objects.filter(group__id=id)
            elif teachers.count() == 1:
                id = teachers.first().id
                type = 'teacher'
                title = get_teacher_name(id).name
                queryset = Lesson.objects.filter(teachers__id=id)
            elif classrooms.count() == 1:
                id = classrooms.first().id
                type = 'classroom'
                title = Classroom.objects.get(pk=id).name
                queryset = Lesson.objects.filter(classrooms__id=id)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif suitable_count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_300_MULTIPLE_CHOICES)
        serializer = ScheduleGroupSerializer(queryset, many=True)

        return Response({
            'id': id,
            'date': self.timestamp(),
            'type': type,
            'title': title,
            'grid': self.transform_result(serializer.data),
        })


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


Search = namedtuple('Search', ('date', 'groups', 'teachers', 'classrooms'))


class SearchViewSet(viewsets.ViewSet):
    """
    Вьюсет для поиска групп, преподавателей и аудиторий без детализации.
    """

    def list(self, request):
        # Текущая дата и время запроса в милисекундах
        now = datetime.date(datetime.now())

        search = Search(
            date=now,
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
