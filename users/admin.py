from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from .models import Profile, Tm_Department, User


# Register your models here.
@admin.register(Tm_Department)
class AdminTm_Department(admin.ModelAdmin):
    list_display = ('department_key', 'department_name', 'order', 'created', 'modified')

@admin.register(User)
class AdminUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'email','departments')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'full_name', 'is_staff')
    search_fields = ('username', 'full_name', 'email')
    filter_horizontal = ('groups', 'user_permissions','departments')

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ('user', 'gender', 'birth_date', 'location', 'favorite_words')
