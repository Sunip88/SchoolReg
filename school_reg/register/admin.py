from django.contrib import admin
from .models import Classes, Subject, Student, Teacher, Parent, Grades, WorkingHours, Schedule, ClassRoom, PresenceList

admin.site.register(Classes)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Parent)
admin.site.register(Grades)
admin.site.register(WorkingHours)
admin.site.register(Schedule)
admin.site.register(ClassRoom)
admin.site.register(PresenceList)

