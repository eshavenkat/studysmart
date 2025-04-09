from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'assignments', views.AssignmentViewSet)
router.register(r'study-sessions', views.StudySessionViewSet)
router.register(r'study-schedules', views.StudyScheduleViewSet)
router.register(r'spaced-repetitions', views.SpacedRepetitionViewSet)
router.register(r'productivity-patterns', views.ProductivityPatternViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('google-calendar/auth/', views.GoogleCalendarAuthView.as_view(), name='google-calendar-auth'),
    path('google-calendar/callback/', views.GoogleCalendarCallbackView.as_view(), name='google-calendar-callback'),
    path('schedule/optimize/', views.OptimizeScheduleView.as_view(), name='optimize-schedule'),
] 