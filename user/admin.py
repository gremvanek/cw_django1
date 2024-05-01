from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import TextInput

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'phone', 'avatar', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    # Переопределение виджета для CharField
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    }


admin.site.register(User, CustomUserAdmin)
