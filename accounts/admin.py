from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DriverProfile, RiderProfile

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra fields', {'fields': ('user_type', 'is_moderator')}),
    )
    list_display = ('username', 'email', 'user_type', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_superuser', 'is_staff', 'is_active')