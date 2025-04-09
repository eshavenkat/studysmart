from django.contrib import admin
from .models import Course, Assignment, StudySession

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('code', 'name', 'description')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'priority', 'difficulty', 'completed')
    list_filter = ('course', 'priority', 'difficulty', 'completed', 'due_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'assignment', 'start_time', 'end_time', 'duration', 'productivity_score')
    list_filter = ('user', 'assignment', 'start_time', 'productivity_score')
    search_fields = ('notes',)
    date_hierarchy = 'start_time'
