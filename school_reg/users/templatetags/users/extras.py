#!/usr/bin/python3.7
from django import template
from django.shortcuts import get_object_or_404

from register.models import Classes, Parent, Announcements, Student

register = template.Library()


@register.filter()
def name_of_class(student):
    student = get_object_or_404(Student, user_id=student.id)
    classes = student.classes
    if classes:
        return classes
    else:
        return "Brak przypisanej klasy"


@register.filter()
def parent_students(user):
    parent = Parent.objects.get(user_id=user.id)
    students = parent.students.all()
    if students:
        return students
    else:
        return "Brak przypisanych uczniów"


@register.simple_tag
def announcements_for_child(child):
    announcements = Announcements.objects.filter(user=child.user)
    return announcements
