from django import forms
from django.forms import fields

from .models import Grades, Adverts, Notice, AdvertsClass, Event


class AddGradeForm(forms.ModelForm):
    class Meta:
        model = Grades
        fields = ['category', 'grade']


class AddAdvertForm(forms.ModelForm):
    class Meta:
        model = Adverts
        fields = ['title', 'text']
        labels = {
            'title': 'tytuł',
            'text': 'treść',
        }


class AddClassAdvertForm(forms.ModelForm):
    class Meta:
        model = AdvertsClass
        fields = ['title', 'text']
        labels = {
            'title': 'tytuł',
            'text': 'treść',
        }


class EditAdvertForm(forms.ModelForm):
    class Meta:
        model = Adverts
        fields = ['title', 'text', 'deleted']
        labels = {
            'title': 'tytuł',
            'text': 'treść',
            'deleted': 'oznaczyć jako usunięte',
        }


class EditClassAdvertForm(forms.ModelForm):
    class Meta:
        model = AdvertsClass
        fields = ['title', 'text', 'deleted']
        labels = {
            'title': 'tytuł',
            'text': 'treść',
            'deleted': 'oznaczyć jako usunięte',
        }


class AddNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['text']
        labels = {
            'text': 'treść uwagi',
        }


class AnswerNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['accepted', 're_text']
        labels = {
            'accepted': 'przyjęte do wiadomości',
            're_text': 'opcjonalny komentarz',
        }


class EditNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['text', 'deleted']
        labels = {
            'text': 'treść uwagi',
            'deleted': 'oznaczyć jako usunięte',
        }


class AddEventForm(forms.ModelForm):
    date_of_event = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Event
        fields = ['title', 'text', 'date_of_event']
        labels = {
            'title': 'tytuł',
            'text': 'opis',
            'date_of_event': 'termin wykonania',
        }
