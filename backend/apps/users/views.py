from datetime import date, timedelta
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import LearningProfile, DailyActivity

class UserMeView(generics.RetrieveUpdateDestroyAPIView):
    """
    Manage the authenticated user's own profile.
    GET: Retrieve full profile.
    PATCH: Update user fields (like avatar) or profile preferences.
    DELETE: Permanently delete the user account (hard delete with cascade).
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Always return the currently logged-in user
        return self.request.user

    def perform_update(self, serializer):
        # Save User fields
        serializer.save()

    def perform_destroy(self, instance):
        """
        Hard delete the user. Django's CASCADE will handle related models:
        - LearningProfile
        - DailyActivity
        - Any other FK pointing to User with on_delete=CASCADE
        """
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        """
        Override to return a clean 204 response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDashboardView(APIView):
    """
    Aggregated dashboard data for the authenticated user.
    Returns stats for the home screen in a single request.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'learning_profile', None)
        
        # Get today's date
        today = date.today()
        
        # Get today's activity
        today_activity = DailyActivity.objects.filter(
            user=user, date=today
        ).first()
        
        today_xp = today_activity.xp_earned if today_activity else 0
        today_minutes = today_activity.minutes_studied if today_activity else 0
        
        # Get last 7 days activity (array of XP per day)
        last_7_days = []
        for i in range(6, -1, -1):  # 6 days ago to today
            day = today - timedelta(days=i)
            activity = DailyActivity.objects.filter(user=user, date=day).first()
            last_7_days.append(activity.xp_earned if activity else 0)
        
        # Build response
        data = {
            'streak': profile.streak_days if profile else 0,
            'longest_streak': profile.longest_streak if profile else 0,
            'current_level': profile.current_level if profile else 1,
            'total_xp': profile.total_xp if profile else 0,
            'today_xp': today_xp,
            'today_minutes': today_minutes,
            'daily_goal_minutes': profile.daily_goal_minutes if profile else 15,
            'daily_goal_met': today_activity.daily_goal_met if today_activity else False,
            'last_7_days_xp': last_7_days,
        }
        
        return Response(data)
