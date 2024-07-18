from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import CustomUser, Notification
from .forms import CustomUserCreationForm,CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.
CustomUser = get_user_model()

class CustomUserAmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'username',
        'email',
        'is_superuser'
    )

admin.site.register(CustomUser, CustomUserAmin)
admin.site.register(Notification)