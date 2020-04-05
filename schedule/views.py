from collections import namedtuple
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
import logging

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
            logger.error(result[0])
            result[lesson.day_of_week-1][lesson.number-1].append(LessonSerializer(lesson).data)
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

        return Response({'time': datetime.datetime.now(), 'grid': self.transform_result(serializer.data)})

    def retrieve_teacher(self, request, id=None):
        """
        Получаем расписание на неделю для преподавателя.
        :param id: первичный ключ преподавателя.
        :return: трансформированный для отображения JSON.
        """
        queryset = Lesson.objects.filter(teachers__id=id)
        serializer = ScheduleGroupSerializer(queryset, many=True)

        return Response({'time': datetime.datetime.now(), 'grid': self.transform_result(serializer.data)})

    def retrieve_classroom(self, request, id=None):
        """
        Получаем расписание на неделю для аудитории.
        :param id: первичный ключ аудитории.
        :return: трансформированный для отображения JSON.
        """
        queryset = Lesson.objects.filter(classrooms__id=id)
        serializer = ScheduleGroupSerializer(queryset, many=True)

        return Response({'time': datetime.datetime.now(), 'grid': self.transform_result(serializer.data)})

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
        print("count: " + str(suitable_count))
        if suitable_count == 1:
            if groups.count() == 1:
                queryset = Lesson.objects.filter(group__id=groups.first().id)
            elif teachers.count() == 1:
                queryset = Lesson.objects.filter(teachers__id=teachers.first().id)
            elif classrooms.count() == 1:
                queryset = Lesson.objects.filter(classrooms__id=classrooms.first().id)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif suitable_count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_300_MULTIPLE_CHOICES)
        serializer = ScheduleGroupSerializer(queryset, many=True)
        return Response({'time': datetime.datetime.now(), 'grid': self.transform_result(serializer.data)})


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
