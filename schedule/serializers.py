from rest_framework import serializers

from .models import *


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Groups
        fields = ('title', 'course', 'date_from', 'date_to', 'evening')


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = ('name', 'group_title', 'type', 'date_from', 'date_to', 'module')


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Teacher
        fields = ('name', )


class AuditorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Auditory
        fields = ('name', 'color')
