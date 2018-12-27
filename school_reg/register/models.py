from django.db import models
from ..users.models import Student, Teacher

GRADES = (
    (1, "1"),
    (1.5, "1+"),
    (1.75, "2-"),
    (2, "2"),
    (2.5, "2+"),
    (2.75, "3-"),
    (3, "3"),
    (3.5, "3+"),
    (3.75, "4-"),
    (4, "4"),
    (4.5, "4+"),
    (4.75, "5-"),
    (5, "5"),
    (5.5, "5+"),
    (5.75, "6-"),
    (6, "6")
)


class ClassOfStudents(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    educator = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    description = models.CharField(max_length=512)


class Subject(models.Model):
    name = models.CharField(max_length=128)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classes = models.ForeignKey(ClassOfStudents, on_delete=models.CASCADE)


class Grades(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.FloatField(choices=GRADES)


class PresenceList(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    day = models.DateField()
    present = models.NullBooleanField()
