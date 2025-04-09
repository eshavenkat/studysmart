from django.db import models
from django.conf import settings
from django.utils import timezone

class StudySchedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignment = models.ForeignKey('core.Assignment', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Schedule - {self.assignment.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    @property
    def is_overdue(self):
        return self.end_time < timezone.now() and not self.completed

class SpacedRepetition(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignment = models.ForeignKey('core.Assignment', on_delete=models.CASCADE)
    next_review_date = models.DateTimeField()
    review_count = models.IntegerField(default=0)
    ease_factor = models.FloatField(default=2.5)
    interval = models.IntegerField(default=1)  # in days
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Spaced Repetition - {self.assignment.title} - Next Review: {self.next_review_date.strftime('%Y-%m-%d')}"

    def update_after_review(self, quality):
        """
        Update the spaced repetition parameters based on review quality
        quality: 0 (complete blackout) to 5 (perfect response)
        """
        if quality < 3:
            # If the response was poor, reset the interval
            self.interval = 1
            self.review_count = 0
        else:
            # Calculate new interval using the SuperMemo 2 algorithm
            self.ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
            if self.review_count == 0:
                self.interval = 1
            elif self.review_count == 1:
                self.interval = 6
            else:
                self.interval = round(self.interval * self.ease_factor)
            
            self.review_count += 1
        
        self.next_review_date = timezone.now() + timezone.timedelta(days=self.interval)
        self.save()

class ProductivityPattern(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ])
    hour = models.IntegerField(choices=[(i, f"{i:02d}:00") for i in range(24)])
    average_productivity = models.FloatField(default=0.0)
    study_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'day_of_week', 'hour']

    def __str__(self):
        return f"Productivity Pattern - {self.user.username} - {self.get_day_of_week_display()} {self.get_hour_display()}"

    def update_productivity(self, new_score):
        """
        Update the average productivity score using exponential moving average
        """
        alpha = 0.1  # Smoothing factor
        self.average_productivity = (alpha * new_score) + ((1 - alpha) * self.average_productivity)
        self.study_count += 1
        self.save()
