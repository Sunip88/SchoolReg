#!/usr/bin/python3.7
from django import template
from datetime import datetime
from register.models import Grades, Teacher, Student, Schedule

register = template.Library()


@register.simple_tag
def grades_all(subject_id, student_id):
    result = []
    sum_grades = 0
    grades_str = []
    grades = Grades.objects.filter(subject_id=subject_id, student_id__exact=student_id)
    for g in grades:
        grades_str.append(str(g.get_grade_display()))
        sum_grades += g.grade
    result.append(", ".join(grades_str))
    result.append(str(sum_grades/grades.count()))
    return result


@register.filter()
def grades_category(grades, category):

    grades_str = []
    for g in grades:
        if g.category.name == category.name:
            grades_str.append(str(g.get_grade_display()))
    result = ", ".join(grades_str)
    return result


@register.filter()
def student_presence(student, subject):
    today = datetime.now().date()
    student = Student.objects.get(user_id=student.user.id)
    presence = student.presencelist_set.filter(subject_id=subject.id, day=today)
    if len(presence) > 0:
        return False
    else:
        return True


@register.filter()
def student_presence_get(student, subject):
    today = datetime.now().date()
    presence = student.presencelist_set.filter(subject_id=subject.id, day=today)
    if presence:
        presence = presence.first()
        return presence.present
    else:
        return False


@register.simple_tag
def grades_category_subject(student, category, subject):
    grades = student.grades_set.filter(subject_id=subject.id)
    grades_str = []
    for g in grades:
        if g.category.name == category.name:
            grades_str.append(str(g.get_grade_display()))
    result = ", ".join(grades_str)
    return result


@register.simple_tag
def teacher_class_subject(subject, detail_class):
    teachers = Teacher.objects.filter(subjects=subject.id, classes=detail_class)
    if teachers:
        result = teachers.first()
    else:
        result = 'Brak wyników'
    return result


@register.simple_tag
def schedule_choice(classes, hours, weekday):
    schedule = Schedule.objects.filter(classes_id=classes.id, weekday=weekday[0], hours=hours)
    if schedule:
        return schedule.first()
    else:
        return []


@register.simple_tag
def schedule_choice_teacher(teacher, hours, weekday):
    schedule = Schedule.objects.filter(weekday=weekday[0], hours=hours, teacher=teacher)
    if schedule:
        return schedule.first()
    else:
        return []


@register.simple_tag
def schedule_choice_room(room, hours, weekday):
    schedule = Schedule.objects.filter(weekday=weekday[0], hours=hours, room=room)
    if schedule:
        return schedule.first()
    else:
        return []


@register.simple_tag
def presence_by_subject(presence, subject):
    result = []
    present = []
    not_present = []
    for pres in presence:
        if pres.subject == subject:
            if pres.present:
                present.append(pres)
            else:
                not_present.append(pres)
    counted_present = len(present)
    counted_not_present = len(not_present)
    counted_all = counted_present + counted_not_present
    result.append(counted_all)
    result.append(counted_present)
    result.append(counted_not_present)
    if counted_present > 0:
        result.append(str(round(counted_present/counted_all * 100, 2)) + ' %')
    else:
        result.append('brak zajec')
    return result


@register.filter()
def subject_today(item, weekday):
    if item.weekday - 1 == weekday:
        return True
    return False
