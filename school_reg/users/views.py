from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from users.models import Profile
from .forms import UserTeacherRegisterForm, UserUpdateForm, ProfileUpdateForm, StudentRegisterForm, \
    ParentRegisterForm, UserParentStudentRegisterForm
from register.models import Teacher
import uuid
import random


class LoginUserView(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "users/login.html"


class LogoutUserView(auth_views.LogoutView):
    template_name = 'users/logout.html'


class RegisterChoiceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'add_user'

    def get(self, request):
        return render(request, 'users/register_choice.html')

    def post(self, request):
        button = request.POST.get('button')
        if button == 'student':
            return redirect('register-students')
        elif button == 'teacher':
            return redirect('register-teacher')
        elif button == 'parent':
            return redirect('register-parent')


class RegisterTeacherView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'add_user'
    form_class = UserTeacherRegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, "users/register.html", {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.role = 2
            user.profile.save()
            Teacher.objects.create(user_id=user.id)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto dla {username} zostało utworzone')
            return redirect('register')
        return render(request, "users/register.html", {"form": form})


class RegisterParentView(LoginRequiredMixin, PermissionRequiredMixin,  View):
    permission_required = 'add_user'
    form_class_u = UserParentStudentRegisterForm
    form_class_p = ParentRegisterForm

    def get(self, request):
        form = self.form_class_u()
        form_p = self.form_class_p()
        return render(request, "users/register.html", {'form': form, 'form_p': form_p})

    def post(self, request):
        form = self.form_class_u(request.POST)
        form_p = self.form_class_p(request.POST)
        if form.is_valid() and form_p.is_valid():
            user = form.save(commit=False)
            random_password = uuid.uuid4().hex
            user.set_password(random_password)
            username = (str(user.first_name[0:3]) + str(user.last_name[0:3])).lower()
            while User.objects.filter(username=username).exists():
                username = username + str(random.randint(0, 100))
            user.username = username
            user.save()
            user.profile.role = 1
            user.profile.temp_password = random_password
            user.profile.save()
            parent = form_p.save(commit=False)
            parent.user_id = user.id
            form_p.save()
            messages.success(request, f'Konto dla {user.username} zostało utworzone')
            return redirect('register')
        return render(request, "users/register.html", {'form': form, 'form_p': form_p})


class RegisterStudentsView(LoginRequiredMixin, PermissionRequiredMixin,  View):
    permission_required = 'add_user'
    form_class_u = UserParentStudentRegisterForm
    form_class_s = StudentRegisterForm

    def get(self, request):
        form = self.form_class_u()
        form_s = self.form_class_s()
        return render(request, "users/register.html", {'form': form, 'form_s': form_s})

    def post(self, request):
        form = self.form_class_u(request.POST)
        form_s = self.form_class_s(request.POST)
        if form.is_valid() and form_s.is_valid():
            year_of_birth = form_s.cleaned_data.get('year_of_birth')
            user = form.save(commit=False)
            random_password = uuid.uuid4().hex
            user.set_password(random_password)
            username = (str(user.first_name[0:3]) + str(user.last_name[0:3]) + str(year_of_birth)[2:]).lower()
            while User.objects.filter(username=username).exists():
                username = username + str(random.randint(0, 100))
            user.username = username
            user.save()
            user.profile.role = 0
            user.profile.temp_password = random_password
            user.profile.save()
            student = form_s.save(commit=False)
            student.user_id = user.id
            form_s.save()
            messages.success(request, f'Konto dla {user.username} zostało utworzone')
            return redirect('register-students')
        return render(request, "users/register.html", {"form": form})


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        if request.user.profile.role != 0:
            p_form = ProfileUpdateForm(instance=request.user.profile)
        role = request.user.profile.role
        return render(request, 'users/profile.html', locals())

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if request.user.profile.role != 0:
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        button = request.POST.get('button')
        if button == 'update':
            if request.user.profile.role != 0:
                if u_form.is_valid() and p_form.is_valid():
                    u_form.save()
                    p_form.save()
                    messages.success(request, f'Twoje konto zostało zmodyfikowane')
                    return redirect('profile')
            else:
                if u_form.is_valid():
                    u_form.save()
                    messages.success(request, f'Twoje konto zostało zmodyfikowane')
                    return redirect('profile')
        elif button == 'change_password':
            return redirect("change-password")


class ChangePasswordView(LoginRequiredMixin, View):

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, "users/user_confirm_password_change.html", {'form': form})

    def post(self, request):
        profile = Profile.objects.get(user_id=request.user.id)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            profile.temp_password = ''
            profile.save()
            user = form.save()
            auth_views.update_session_auth_hash(request, user)
            messages.success(request, "Hasło zostało zmienione")
            return redirect("profile")
        else:
            messages.error(request, "Prosze wprowadzić poprawne dane")
        return render(request, "users/user_confirm_password_change.html", locals())


class PasswordOnlineView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.profile.role != 2:
            if request.user.profile.temp_password != '':
                return HttpResponse(str(1))
        return HttpResponse(str(0))
