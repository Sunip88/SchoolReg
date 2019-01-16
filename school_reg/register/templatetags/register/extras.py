#!/usr/bin/python3.7
from django import template

from register.models import Grades

register = template.Library()


@register.filter()
def grades_all(subject_id, student_id):
    sum_grades = 0
    grades_str = []
    grades = Grades.objects.filter(subject_id=subject_id, student_id__exact=student_id)
    for g in grades:
        grades_str.append(str(g.get_grade_display()))
        sum_grades += g.grade
    result = ", ".join(grades_str) + " // " + str(sum_grades/grades.count())
    return result

