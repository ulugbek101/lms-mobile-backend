from django.contrib import admin
from django.contrib.auth.models import Group as UserGroup
from django.contrib.auth import get_user_model

from .models import Admin, Teacher, Parent, Student, Subject, Group, Lesson, Attendance

User = get_user_model()

admin.site.unregister(UserGroup)
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Teacher)
admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(Lesson)
admin.site.register(Attendance)
