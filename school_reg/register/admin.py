from django.contrib import admin
from .models import Classes, Subject, Student, Teacher, Parent, Grades


admin.site.register(Classes)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Parent)
admin.site.register(Grades)
