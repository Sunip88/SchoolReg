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

WEEKDAYS = [
    (1, 'Poniedziałek'),
    (2, 'Wtorek'),
    (3, 'Środa'),
    (4, 'Czwartek'),
    (5, 'Piątek'),
]


class Classes(models.Model):
    educator = models.ForeignKey('register.Teacher', on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return f'{self.name}'


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


class ClassRoom(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class WorkingHours(models.Model):
    nr = models.IntegerField()
    hours = models.CharField(max_length=16)

    def __str__(self):
        return self.hours


class Schedule(models.Model):
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    hours = models.ForeignKey(WorkingHours, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS)


class Adverts(models.Model):
    text = models.TextField()
    title = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)


class AdvertsClass(models.Model):
    text = models.TextField()
    title = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)


class Notice(models.Model):
    text = models.CharField(max_length=256)
    from_user = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    to_user = models.ForeignKey(Student, on_delete=models.CASCADE)
    accepted = models.NullBooleanField()
    re_text = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    deleted = models.BooleanField(default=False)


class Announcements(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
