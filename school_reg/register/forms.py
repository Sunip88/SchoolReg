from django import forms
from .models import Student, Parent, Classes, Grades, PresenceList, Adverts, Notice


class AddGradeForm(forms.ModelForm):
    class Meta:
        model = Grades
        fields = ['category', 'grade']


class PresenceForm(forms.ModelForm):
    class Meta:
        model = PresenceList
        fields = ['present']


class AddAdvertForm(forms.ModelForm):
    class Meta:
        model = Adverts
        fields = ['title', 'text']


class AddNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['text']
