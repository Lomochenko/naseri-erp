from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'email', 'is_staff', 'is_manager', 'is_active')
    list_filter = ('is_staff', 'is_manager', 'is_active')
    search_fields = ('phone_number', 'first_name', 'last_name', 'email')
    ordering = ('phone_number',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_manager', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_manager'),
        }),
    )
