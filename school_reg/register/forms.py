from django import forms
from .models import Student, Parent, Classes, Grades, PresenceList


class AddGradeForm(forms.ModelForm):
    class Meta:
        model = Grades
        fields = ['category', 'grade']


class PresenceForm(forms.ModelForm):
    class Meta:
        model = PresenceList
        fields = ['present']
