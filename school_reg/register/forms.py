from django import forms
from django.forms import fields

from .models import Grades, Adverts, Notice, AdvertsClass, Event


class AddGradeForm(forms.ModelForm):
    class Meta:
        model = Grades
        fields = ['category', 'grade']
        labels = {
            'category': 'kategoria',
            'grade': 'ocena'
        }


class AddAdvertForm(forms.ModelForm):
    class Meta:
        model = Adverts
        fields = ['title', 'text']
        labels = {
            'title': 'tytuł',
            'text': 'treść',
        }
        help_texts = {
            'title': 'Podaj tytuł ogłoszenia',
            'text': 'Podaj treść ogłoszenia'
        }


class AddClassAdvertForm(forms.ModelForm):
    class Meta:
        model = AdvertsClass
        fields = ['title', 'text']
        labels = {
            'title': 'tytuł',
            'text': 'treść',
        }
        help_texts = {
            'title': 'Podaj tytuł ogłoszenia klasowego',
            'text': 'Podaj treść ogłoszenia klasowego'
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
        help_texts = {
            'title': 'Zmień tytuł ogłoszenia',
            'text': 'Zmień treść ogłoszenia'
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
        help_texts = {
            'title': 'Zmień tytuł ogłoszenia klasowego',
            'text': 'Zmień treść ogłoszenia klasowego'
        }


class AddNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['text']
        labels = {
            'text': 'treść',
        }
        help_texts = {
            'text': 'Podaj treść uwagi'
        }


class AnswerNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['accepted', 're_text']
        labels = {
            'accepted': 'przyjęte do wiadomości',
            're_text': 'treść',
        }
        help_texts = {
            're_text': 'Podaj treść komentarza'
        }


class EditNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['text', 'deleted']
        labels = {
            'text': 'treść',
            'deleted': 'oznaczyć jako usunięte',
        }
        help_texts = {
            'text': 'Zmień treść uwagi'
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
        help_texts = {
            'title': 'Podaj tytuł wydarzenia',
            'text': 'Podaj treść wydarzenia',
        }
