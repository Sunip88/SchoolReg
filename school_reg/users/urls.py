from django.urls import path
from .views import LoginUserView, LogoutUserView, RegisterUserView, ProfileView, ChangePasswordView, \
    ConfirmDeleteUserView

urlpatterns = [
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('delete_user/<int:pk>/', ConfirmDeleteUserView.as_view(), name='delete-user'),
]