from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


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


class Classes(models.Model):
    educator = models.ForeignKey('register.Teacher', on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return f'{self.name} - {self.educator}'


class Subject(models.Model):
    name = models.CharField(max_length=128)
    classes = models.ManyToManyField(Classes)

    def __str__(self):
        return f'{self.name}'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Student(models.Model):
    year_of_birth = models.PositiveIntegerField(validators=[MinValueValidator(1000), MaxValueValidator(3000)],
                                                null=True)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class GradeCategory(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Grades(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    category = models.ForeignKey(GradeCategory, on_delete=models.CASCADE)
    grade = models.FloatField(choices=GRADES)

    def __str__(self):
        return f'{self.subject} - {self.student} - {self.grade}'


class PresenceList(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    day = models.DateField()
    present = models.NullBooleanField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
