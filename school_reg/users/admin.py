from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'image', 'role', 'temp_password', 'phone']
    list_filter = ['role']
