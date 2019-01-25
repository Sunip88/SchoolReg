from django import forms
from .models import Grades, Adverts, Notice, AdvertsClass


class AddGradeForm(forms.ModelForm):
    class Meta:
        model = Grades
        fields = ['category', 'grade']


class AddAdvertForm(forms.ModelForm):
    class Meta:
        model = Adverts
        fields = ['title', 'text']


class AddClassAdvertForm(forms.ModelForm):
    class Meta:
        model = AdvertsClass
        fields = ['title', 'text']


class EditAdvertForm(forms.ModelForm):
    class Meta:
        model = Adverts
        fields = ['title', 'text', 'deleted']


class EditClassAdvertForm(forms.ModelForm):
    class Meta:
        model = AdvertsClass
        fields = ['title', 'text', 'deleted']


class AddNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['text']


class AnswerNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['accepted', 're_text']


class EditNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['text', 'deleted']
