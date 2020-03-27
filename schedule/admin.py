from django.contrib import admin

from schedule.forms import *
from schedule.models import *
from django.contrib.auth.models import User, Group

admin.site.unregister(User)
admin.site.unregister(Group)


# class LessonAdmin(admin.ModelAdmin):
#     form = LessonFrom


admin.site.register(Groups)
admin.site.register(Teacher)
admin.site.register(Classroom)
admin.site.register(Lesson)
