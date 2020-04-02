import datetime

from rest_framework import serializers

from .models import *


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ('id', 'name', 'is_evening')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name')


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ('id', 'name', 'color')


class SearchSerializer(serializers.Serializer):
    groups = GroupSerializer(many=True)
    teachers = TeacherSerializer(many=True)
    classrooms = ClassroomSerializer(many=True)


class TimestampField(serializers.Field):
    def to_representation(self, value):
        epoch = datetime.date(1970, 1, 1)
        return int((value - epoch).total_seconds())


class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = ('name', )


class LessonSerializer(serializers.ModelSerializer):
    # UNIX timestamp для сравнения и сортировки дат
    date_from = TimestampField()
    date_to = TimestampField()
    # Django Model.get_FOO_display
    week = serializers.CharField(source='get_week_display')
    day_of_week = serializers.CharField(source='get_day_of_week_display')
    # Получаем по внешнему ключу название типа пары с помощью метода
    type = serializers.SerializerMethodField(source='get_type')
    group = GroupSerializer(many=False, read_only=True)
    teachers = TeacherSerializer(many=True, read_only=True)
    classrooms = ClassroomSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'teachers', 'group', 'classrooms', 'type', 'date_from', 'date_to', 'number', 'day_of_week', 'week')

    def get_type(self, obj):
        return obj.type.name


class ScheduleGroupSerializer(serializers.ModelSerializer):
    # teachers = TeacherSerializer(many=True)
    # classrooms = ClassroomSerializer(many=True)
    #
    # class Meta:
    #     model = Lesson
    #     fields = ('name', 'day', 'teachers', 'classrooms', 'type', 'date_from', 'date_to')

    def to_representation(self, instance):
        """
        Оверрайдим метод для того, чтобы возвращать данные в более удобном
        для парсинга виде (dict вместо OrderedDict).
        :return: dict(instance)
        """
        return instance
