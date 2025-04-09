from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'preferred_study_time', 'learning_style', 'productivity_score')
    list_filter = ('preferred_study_time', 'learning_style')
    fieldsets = UserAdmin.fieldsets + (
        ('Study Preferences', {'fields': (
            'preferred_study_time',
            'study_duration',
            'break_duration',
            'learning_style',
            'productivity_score',
            'google_calendar_token'
        )}),
    )
