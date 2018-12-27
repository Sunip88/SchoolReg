from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, FormView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views, login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, LoginForm


class LoginUserView(View):
    form_class = LoginForm

    def get(self, request):
        return render(request, 'users/login.html', {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = User.objects.filter(email=email.lower()).first()
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                messages.warning(request, 'Błędny login lub hasło')
        return render(request, 'users/login.html', {'form': self.form_class})


class LogoutUserView(auth_views.LogoutView):
    template_name = 'users/logout.html'


class RegisterUserView(View):
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, "users/register.html", {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Konto dla {email} zostało utworzone')
            return redirect('login')
        return render(request, "users/register.html", {"form": form})


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'users/profile.html', locals())

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        button = request.POST.get('button')
        if button == 'update':
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Twoje konto zostało zmodyfikowane')
                return redirect('profile')
        elif button == 'delete':
            user = request.user
            return redirect("delete-user", pk=user.id)
        elif button == 'change_password':
            return redirect("change-password")


class ChangePasswordView(LoginRequiredMixin, View):

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, "users/user_confirm_password_change.html", locals())

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            auth_views.update_session_auth_hash(request, user)
            messages.success(request, "Hasło zostało zmienione")
            return redirect("profile")
        else:
            messages.error(request, "Prosze wprowadzić poprawne dane")
        return render(request, "users/user_confirm_password_change.html", locals())


class ConfirmDeleteUserView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy("login")
    template_name = 'users/user_confirm_delete.html'

    def test_func(self):
        user = self.get_object()
        if self.request.user.id == user.id:
            return True
        return False
