from django import forms
from django.forms import ModelChoiceField

from schedule.models import *


class LessonFrom(forms.ModelForm):
    group = ModelChoiceField(queryset=Groups.objects, empty_label=None)
    type = forms.ChoiceField(choices=Lesson.TYPES)
    module = forms.ChoiceField(choices=Lesson.MODULES)
    teachers = forms.ModelMultipleChoiceField(queryset=Teacher.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'
