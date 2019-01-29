from django.urls import path
from .views import LoginUserView, LogoutUserView, RegisterTeacherView, ProfileView, ChangePasswordView, \
    RegisterChoiceView, RegisterParentView, RegisterStudentsView, PasswordOnlineView

urlpatterns = [
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterChoiceView.as_view(), name='register'),
    path('register_teacher/', RegisterTeacherView.as_view(), name='register-teacher'),
    path('register_parent/', RegisterParentView.as_view(), name='register-parent'),
    path('register_students/', RegisterStudentsView.as_view(), name='register-students'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('password_online/', PasswordOnlineView.as_view(), name='password-online'),
]