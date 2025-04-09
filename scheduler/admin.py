from django.contrib import admin
from .models import StudySchedule, SpacedRepetition, ProductivityPattern

@admin.register(StudySchedule)
class StudyScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'assignment', 'start_time', 'end_time', 'completed')
    list_filter = ('user', 'assignment', 'completed', 'start_time')
    search_fields = ('assignment__title',)
    date_hierarchy = 'start_time'

@admin.register(SpacedRepetition)
class SpacedRepetitionAdmin(admin.ModelAdmin):
    list_display = ('user', 'assignment', 'next_review_date', 'review_count', 'interval')
    list_filter = ('user', 'assignment', 'next_review_date')
    search_fields = ('assignment__title',)
    date_hierarchy = 'next_review_date'

@admin.register(ProductivityPattern)
class ProductivityPatternAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'hour', 'average_productivity', 'study_count')
    list_filter = ('user', 'day_of_week', 'hour')
    search_fields = ('user__username',)
