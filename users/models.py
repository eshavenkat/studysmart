from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Study preferences
    preferred_study_time = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
            ('night', 'Night'),
        ],
        default='morning'
    )
    
    study_duration = models.IntegerField(
        help_text="Preferred study session duration in minutes",
        default=45
    )
    
    break_duration = models.IntegerField(
        help_text="Preferred break duration in minutes",
        default=15
    )
    
    # Productivity tracking
    productivity_score = models.FloatField(
        help_text="Overall productivity score (0-100)",
        default=0.0
    )
    
    # Learning style preferences
    learning_style = models.CharField(
        max_length=20,
        choices=[
            ('visual', 'Visual'),
            ('auditory', 'Auditory'),
            ('reading', 'Reading/Writing'),
            ('kinesthetic', 'Kinesthetic'),
        ],
        default='visual'
    )
    
    # Calendar integration
    google_calendar_token = models.TextField(
        blank=True,
        null=True,
        help_text="Google Calendar OAuth token"
    )
    
    def __str__(self):
        return self.username
