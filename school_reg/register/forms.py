from django import forms
from .models import Student, Parent, Classes, Grades


class AddGradeForm(forms.ModelForm):
    class Meta:
        model = Grades
        fields = ['category', 'grade']

