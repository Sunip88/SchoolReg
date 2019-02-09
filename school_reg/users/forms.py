from django import forms
from django.contrib.auth.models import User
from register.models import Student, Parent
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class UserTeacherRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'login',
            'first_name': 'imię',
            'last_name': 'nazwisko',
            'email': 'email',
        }
        help_texts = {
            'username': 'Podaj nazwę użytkownika',
            'first_name': 'Podaj imię użytkownika',
            'last_name': 'Podaj nazwisko użytkownika',
            'email': 'Podaj email użytkownika',
        }


class ParentRegisterForm(forms.ModelForm):

    class Meta:
        model = Parent
        fields = ['students']

    def __init__(self, *args, **kwargs):
        super(ParentRegisterForm, self).__init__(*args, **kwargs)
        self.fields['students'].required = False
        self.fields['students'].label = 'dzieci'
        self.fields['students'].widget = forms.CheckboxSelectMultiple()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        labels = {
            'email': 'email'
        }
        help_texts = {
            'email': 'Podaj nowy email',
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone']
        labels = {
            'image': 'zdjęcie',
            'phone': 'telefon',
        }
        help_texts = {
            'image': 'Podaj nowe zdjęcie',
            'phone': 'Podaj nowy telefon',
        }


class UserParentStudentRegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': 'imię',
            'last_name': 'nazwisko',
        }
        help_texts = {
            'first_name': 'Podaj imię użytkownika',
            'last_name': 'Podaj nazwisko użytkownika',
        }


class StudentRegisterForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['year_of_birth', 'classes']
        labels = {
            'year_of_birth': 'rok urodzenia',
            'classes': 'klasa',
        }
        help_texts = {
            'year_of_birth': 'Podaj rok urodzenia użytkownika',
        }
