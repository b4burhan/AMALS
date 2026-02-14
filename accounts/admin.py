from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'country', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone', 'city']
    list_filter = ['country', 'created_at']
