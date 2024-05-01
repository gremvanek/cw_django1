from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'phone', 'avatar', 'country', 'is_verified', 'have_permissions')
    search_fields = ('email', 'username', 'phone', 'country')
    list_filter = ('is_verified', 'have_permissions')
    readonly_fields = ('verification_code',)

    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'phone', 'avatar', 'country')
        }),
        ('Permissions', {
            'fields': ('is_verified', 'have_permissions')
        }),
        ('Verification', {
            'fields': ('verification_code',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone', 'avatar', 'country', 'is_verified', 'have_permissions', 'verification_code'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Existing object
            return self.readonly_fields + ('email', 'username')
        return self.readonly_fields
