from django import forms
from django.forms import ModelChoiceField

from schedule.models import Lesson, Groups


class LessonFrom(forms.ModelForm):
    group_title = ModelChoiceField(queryset=Groups.objects, empty_label=None)
    type = forms.ChoiceField(choices=Lesson.TYPES)
    module = forms.ChoiceField(choices=Lesson.MODULES)

    class Meta:
        model = Lesson
        fields = '__all__'
