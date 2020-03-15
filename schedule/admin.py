from django.contrib import admin
from schedule.models import Groups
from django.contrib.auth.models import User, Group


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Groups)

