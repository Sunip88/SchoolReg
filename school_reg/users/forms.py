from django import forms
from django.contrib.auth.models import User
from register.models import Student, Parent
from .models import Profile, Messages
from django.contrib.auth.forms import UserCreationForm


class UserTeacherRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ParentRegisterForm(forms.ModelForm):

    class Meta:
        model = Parent
        fields = ['students']

    def __init__(self, *args, **kwargs):
        super(ParentRegisterForm, self).__init__(*args, **kwargs)
        self.fields['students'].required = False
        self.fields['students'].widget = forms.CheckboxSelectMultiple()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class UserParentStudentRegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class StudentRegisterForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['year_of_birth', 'classes']


class MessagesAddForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['content', 'send_to']
