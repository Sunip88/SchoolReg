from django.contrib import admin
from .models import Classes, Subject, Student, Teacher, Parent, Grades, WorkingHours, Schedule, ClassRoom, PresenceList, \
    GradeCategory, Adverts, AdvertsClass, Notice, Announcements, Event


@admin.register(Classes)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'educator', 'name', 'description']


@admin.register(Subject)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']


@admin.register(Student)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'year_of_birth', 'classes']
    list_filter = ['year_of_birth', 'classes']


@admin.register(Teacher)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


@admin.register(Parent)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


@admin.register(Grades)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'student', 'category', 'grade']
    list_filter = ['subject', 'category', 'student']


@admin.register(GradeCategory)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(WorkingHours)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'nr', 'start_time', 'end_time']


@admin.register(Schedule)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'classes', 'subject', 'room', 'teacher', 'hours', 'weekday']
    list_filter = ['classes', 'subject', 'room', 'teacher', 'hours', 'weekday']


@admin.register(ClassRoom)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(PresenceList)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'day', 'present', 'subject']
    list_filter = ['present']


def content_display_thirty_signs(obj):
    return str(obj.text)[0:30]


content_display_thirty_signs.short_description = 'text'


def deleted(model_admin, request, query_set):
    query_set.update(deleted=True)


deleted.short_description = "Ukryj element w widoku"


@admin.register(Adverts)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date', content_display_thirty_signs, 'author', 'deleted']
    list_filter = ['deleted']
    actions = [deleted, ]


@admin.register(AdvertsClass)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'classes', 'date', content_display_thirty_signs, 'author', 'deleted']
    list_filter = ['deleted', 'classes']
    actions = [deleted, ]


@admin.register(Notice)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'to_user', 'accepted', content_display_thirty_signs, 're_text', 'date', 'deleted']
    list_filter = ['deleted', 'accepted', 'from_user']
    actions = [deleted, ]


@admin.register(Announcements)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'date', 'read', content_display_thirty_signs, 'deleted']
    list_filter = ['read', 'deleted']
    actions = [deleted, ]


@admin.register(Event)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'schedule', 'date_set', 'date_of_event', 'title', content_display_thirty_signs, 'deleted']
    list_filter = ['date_of_event', 'deleted']
    actions = [deleted, ]
