from rest_framework import serializers

from .models import *


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ('id', 'title', 'evening')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name', )


class AuditorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditory
        fields = ('id', 'name', 'color')


class SearchSerializer(serializers.Serializer):
    groups = GroupSerializer(many=True)
    teachers = TeacherSerializer(many=True)
    classrooms = AuditorySerializer(many=True)


class LessonSerializer(serializers.ModelSerializer):
    # group = GroupSerializer()
    teachers = TeacherSerializer(many=True)
    classrooms = AuditorySerializer(many=True)
    # day = serializers.SerializerMethodField('get_temp')
    #
    # def get_temp(self, obj):
    #     return {obj.day: [obj.name, obj.group]}

    class Meta:
        model = Lesson
        fields = ('name', 'teachers', 'classrooms', 'type', 'date_from', 'date_to', 'module')


class GroupLessonSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True)
    classrooms = AuditorySerializer(many=True)

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'day', 'teachers', 'classrooms', 'type', 'date_from', 'date_to', 'module')

    def to_representation(self, instance):
        # temp = super().to_representation(instance)

        return instance
