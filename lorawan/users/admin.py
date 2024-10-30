from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from web_app.models import Sensor

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'first_name', 'last_name',]
    fieldsets = (
        (None, {
            'fields': ('username',)
        }),
        (None, {
            'fields': ('password',)
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name',)
        }),
        ('Additional info', {
            'fields': ('filial', 'department',)
        })
    )

admin.site.register(User, CustomUserAdmin)
