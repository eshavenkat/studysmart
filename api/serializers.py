from rest_framework import serializers
from users.models import User
from core.models import Course, Assignment, StudySession
from scheduler.models import StudySchedule, SpacedRepetition, ProductivityPattern

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'preferred_study_time', 
                 'study_duration', 'break_duration', 'productivity_score',
                 'learning_style')
        read_only_fields = ('id', 'productivity_score')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'code', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class AssignmentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = Assignment
        fields = ('id', 'title', 'course', 'course_name', 'description',
                 'due_date', 'priority', 'difficulty', 'estimated_duration',
                 'completed', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class StudySessionSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    
    class Meta:
        model = StudySession
        fields = ('id', 'assignment', 'assignment_title', 'start_time',
                 'end_time', 'duration', 'productivity_score', 'notes',
                 'created_at')
        read_only_fields = ('id', 'created_at')

class StudyScheduleSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    
    class Meta:
        model = StudySchedule
        fields = ('id', 'assignment', 'assignment_title', 'start_time',
                 'end_time', 'completed', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class SpacedRepetitionSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    
    class Meta:
        model = SpacedRepetition
        fields = ('id', 'assignment', 'assignment_title', 'next_review_date',
                 'review_count', 'ease_factor', 'interval', 'created_at',
                 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class ProductivityPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductivityPattern
        fields = ('id', 'day_of_week', 'hour', 'average_productivity',
                 'study_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at') 