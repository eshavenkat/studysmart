from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from .serializers import (
    UserSerializer, CourseSerializer, AssignmentSerializer,
    StudySessionSerializer, StudyScheduleSerializer,
    SpacedRepetitionSerializer, ProductivityPatternSerializer
)
from users.models import User
from core.models import Course, Assignment, StudySession
from scheduler.models import StudySchedule, SpacedRepetition, ProductivityPattern

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return User.objects.filter(id=self.request.user.id)
        return super().get_queryset()

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Assignment.objects.filter(course__user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        assignment = self.get_object()
        assignment.completed = True
        assignment.save()
        return Response({'status': 'assignment completed'})

class StudySessionViewSet(viewsets.ModelViewSet):
    serializer_class = StudySessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        session = serializer.save(user=self.request.user)
        # Update productivity pattern
        pattern, created = ProductivityPattern.objects.get_or_create(
            user=self.request.user,
            day_of_week=session.start_time.weekday(),
            hour=session.start_time.hour
        )
        pattern.update_productivity(session.productivity_score)

class StudyScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = StudyScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudySchedule.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SpacedRepetitionViewSet(viewsets.ModelViewSet):
    serializer_class = SpacedRepetitionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SpacedRepetition.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        repetition = self.get_object()
        quality = request.data.get('quality', 3)
        repetition.update_after_review(quality)
        return Response({'status': 'review recorded'})

class ProductivityPatternViewSet(viewsets.ModelViewSet):
    serializer_class = ProductivityPatternSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProductivityPattern.objects.filter(user=self.request.user)

class GoogleCalendarAuthView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Implement Google Calendar OAuth flow
        pass

class GoogleCalendarCallbackView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Handle Google Calendar OAuth callback
        pass

class OptimizeScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Get user's assignments and preferences
        assignments = Assignment.objects.filter(
            course__user=request.user,
            completed=False
        ).order_by('due_date')
        
        # Get user's productivity patterns
        patterns = ProductivityPattern.objects.filter(user=request.user)
        
        # Create features for the model
        features = []
        for assignment in assignments:
            features.append({
                'due_date': (assignment.due_date - timezone.now()).days,
                'priority': {'low': 1, 'medium': 2, 'high': 3}[assignment.priority],
                'difficulty': {'easy': 1, 'medium': 2, 'hard': 3}[assignment.difficulty],
                'estimated_duration': assignment.estimated_duration,
            })
        
        # Create target values (productivity scores)
        targets = [pattern.average_productivity for pattern in patterns]
        
        if len(features) < 2:
            return Response({
                'error': 'Not enough data to optimize schedule'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Train a simple model to predict optimal study times
        model = RandomForestRegressor(n_estimators=100)
        model.fit(features, targets)
        
        # Generate optimal schedule
        schedule = []
        current_time = timezone.now()
        
        for assignment in assignments:
            # Find the best time slot based on user's preferences and patterns
            best_time = self._find_best_time_slot(
                current_time,
                assignment.estimated_duration,
                patterns
            )
            
            schedule.append({
                'assignment': assignment.id,
                'start_time': best_time,
                'end_time': best_time + timedelta(minutes=assignment.estimated_duration)
            })
            
            current_time = best_time + timedelta(minutes=assignment.estimated_duration)
        
        # Create study schedules
        for item in schedule:
            StudySchedule.objects.create(
                user=request.user,
                assignment_id=item['assignment'],
                start_time=item['start_time'],
                end_time=item['end_time']
            )
        
        return Response({
            'schedule': schedule
        })

    def _find_best_time_slot(self, start_time, duration, patterns):
        # Find the best time slot based on productivity patterns
        best_score = -1
        best_time = start_time
        
        # Check next 24 hours for optimal time slot
        for hour in range(24):
            current_time = start_time.replace(hour=hour, minute=0, second=0, microsecond=0)
            
            # Get productivity pattern for this time
            pattern = patterns.filter(
                day_of_week=current_time.weekday(),
                hour=current_time.hour
            ).first()
            
            if pattern and pattern.average_productivity > best_score:
                best_score = pattern.average_productivity
                best_time = current_time
        
        return best_time
