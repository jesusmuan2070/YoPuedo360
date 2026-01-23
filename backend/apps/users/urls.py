from django.urls import path
from .views import (
    UserMeView, UserDashboardView, RecordSessionView,
    ActivityHistoryView, StreakDetailView, XPHistoryView, UserSettingsView
)

urlpatterns = [
    path('me/', UserMeView.as_view(), name='user_me'),
    path('me/dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('me/record-session/', RecordSessionView.as_view(), name='record_session'),
    path('me/activity/', ActivityHistoryView.as_view(), name='activity_history'),
    path('me/streaks/', StreakDetailView.as_view(), name='streak_detail'),
    path('me/xp-history/', XPHistoryView.as_view(), name='xp_history'),
    path('me/settings/', UserSettingsView.as_view(), name='user_settings'),
]
