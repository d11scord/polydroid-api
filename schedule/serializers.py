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


class LessonSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=False, read_only=True)
    teachers = TeacherSerializer(many=True, read_only=True)
    classrooms = ClassroomSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ('name', 'teachers', 'group', 'classrooms', 'type', 'date_from', 'date_to', 'number', 'week')


class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = ('id', 'name')


class GroupLessonSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True)
    classrooms = ClassroomSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'day', 'teachers', 'classrooms', 'type', 'date_from', 'date_to')

    def to_representation(self, instance):
        """
        Оверрайдим метод для того, чтобы возвращать данные в более удобном
        для парсинга виде (dict вместо OrderedDict).
        :return: dict(instance)
        """
        return instance
