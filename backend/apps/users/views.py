from datetime import date, timedelta
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RecordSessionSerializer
from .models import LearningProfile, DailyActivity
from .services.daily_activity_service import DailyActivityService

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


class RecordSessionView(APIView):
    """
    Record a study session for the authenticated user.
    
    POST /api/v1/users/me/record-session/
    
    This endpoint:
    - Updates daily minutes studied
    - Tracks XP earned today
    - Detects when daily goal is completed
    - Returns a celebration flag for frontend animations
    
    Request body:
    {
        "minutes": 5,           # Required: 1-180
        "xp_earned": 25,        # Optional: XP from this session
        "activity_type": "exercise"  # Optional: exercise/lesson/vocabulary/grammar/conversation
    }
    
    Response:
    {
        "date": "2026-01-23",
        "minutes_studied": 15,
        "daily_goal": 20,
        "daily_goal_met": true,
        "just_completed_goal": true,  # 🎉 Show celebration!
        "bonus_xp_awarded": 25,
        "progress_percent": 75,
        "streak_days": 7,
        "total_xp": 1500
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = RecordSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        minutes = serializer.validated_data['minutes']
        xp_earned = serializer.validated_data.get('xp_earned', 0)
        
        # Record the activity
        result = DailyActivityService.record_activity(
            user=user,
            minutes=minutes,
            xp_earned=xp_earned
        )
        
        # Add streak and XP info from profile
        profile = getattr(user, 'learning_profile', None)
        result['streak_days'] = profile.streak_days if profile else 0
        result['total_xp'] = profile.total_xp if profile else 0
        result['current_level'] = profile.current_level if profile else 1
        
        return Response(result, status=status.HTTP_200_OK)


class ActivityHistoryView(APIView):
    """
    Get paginated activity history for calendar/heatmap display.
    
    GET /api/v1/users/me/activity/
    
    Query params:
        - days: Number of days to fetch (default 30, max 365)
        - page: Page number for pagination
    
    Response:
    {
        "results": [
            {"date": "2026-01-23", "minutes": 15, "xp": 75, "goal_met": true},
            ...
        ],
        "total_days": 30,
        "days_active": 25,
        "total_minutes": 450,
        "total_xp": 2250
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        days = min(int(request.query_params.get('days', 30)), 365)
        
        # Get activities for the requested period
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)
        
        activities = DailyActivity.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('-date')
        
        # Build results
        results = []
        for activity in activities:
            results.append({
                'date': str(activity.date),
                'minutes': activity.minutes_studied,
                'xp': activity.xp_earned,
                'goal_met': activity.daily_goal_met,
                'exercises': activity.exercises_completed,
                'lessons': activity.lessons_completed,
            })
        
        # Calculate aggregates
        total_minutes = sum(a.minutes_studied for a in activities)
        total_xp = sum(a.xp_earned for a in activities)
        days_active = len([a for a in activities if a.minutes_studied > 0])
        
        return Response({
            'results': results,
            'total_days': days,
            'days_active': days_active,
            'total_minutes': total_minutes,
            'total_xp': total_xp,
        })


class StreakDetailView(APIView):
    """
    Get detailed streak information for motivational UI.
    
    GET /api/v1/users/me/streaks/
    
    Response:
    {
        "current_streak": 7,
        "longest_streak": 15,
        "streak_start_date": "2026-01-17",
        "weekly_activity": [true, true, false, true, true, true, true],
        "is_at_risk": false
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        profile = getattr(user, 'learning_profile', None)
        
        # Calculate streak start date
        current_streak = profile.streak_days if profile else 0
        streak_start_date = None
        if current_streak > 0:
            streak_start_date = str(date.today() - timedelta(days=current_streak - 1))
        
        # Get weekly activity pattern (last 7 days)
        today = date.today()
        weekly_activity = []
        for i in range(6, -1, -1):  # 6 days ago to today
            day = today - timedelta(days=i)
            activity = DailyActivity.objects.filter(user=user, date=day).first()
            was_active = activity and activity.minutes_studied >= 5  # 5 min minimum
            weekly_activity.append(was_active)
        
        # Check if streak is at risk (no activity today yet)
        today_activity = DailyActivity.objects.filter(user=user, date=today).first()
        is_at_risk = current_streak > 0 and (
            not today_activity or today_activity.minutes_studied < 5
        )
        
        return Response({
            'current_streak': current_streak,
            'longest_streak': profile.longest_streak if profile else 0,
            'streak_start_date': streak_start_date,
            'weekly_activity': weekly_activity,
            'is_at_risk': is_at_risk,
        })


class XPHistoryView(APIView):
    """
    Get XP earning history for animations and progress display.
    
    GET /api/v1/users/me/xp-history/
    
    Query params:
        - days: Number of days (default 7)
    
    Response:
    {
        "current_level": 5,
        "total_xp": 4500,
        "xp_to_next_level": 500,
        "level_progress_percent": 50,
        "daily_xp": [
            {"date": "2026-01-23", "xp": 75},
            ...
        ]
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        profile = getattr(user, 'learning_profile', None)
        days = min(int(request.query_params.get('days', 7)), 30)
        
        # Calculate level progress
        total_xp = profile.total_xp if profile else 0
        current_level = profile.current_level if profile else 1
        
        # XP needed for current level threshold
        xp_for_current_level = (current_level - 1) * 1000
        xp_for_next_level = current_level * 1000
        xp_in_current_level = total_xp - xp_for_current_level
        xp_needed_for_level = 1000  # Each level requires 1000 XP
        
        level_progress_percent = min(100, int((xp_in_current_level / xp_needed_for_level) * 100))
        xp_to_next_level = max(0, xp_for_next_level - total_xp)
        
        # Get daily XP for chart
        today = date.today()
        daily_xp = []
        for i in range(days - 1, -1, -1):
            day = today - timedelta(days=i)
            activity = DailyActivity.objects.filter(user=user, date=day).first()
            daily_xp.append({
                'date': str(day),
                'xp': activity.xp_earned if activity else 0
            })
        
        return Response({
            'current_level': current_level,
            'total_xp': total_xp,
            'xp_to_next_level': xp_to_next_level,
            'xp_in_current_level': xp_in_current_level,
            'level_progress_percent': level_progress_percent,
            'daily_xp': daily_xp,
        })


class UserSettingsView(APIView):
    """
    Manage user preferences and notification settings.
    
    GET /api/v1/users/me/settings/
    PATCH /api/v1/users/me/settings/
    
    Settings available:
    - daily_goal_minutes: Daily study goal (5-120)
    - preferred_ai_provider: AI provider preference
    - notifications_enabled: Push notification toggle (future)
    - reminder_time: Daily reminder time (future)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        profile = getattr(user, 'learning_profile', None)
        
        return Response({
            'daily_goal_minutes': profile.daily_goal_minutes if profile else 15,
            'learning_goal': profile.learning_goal if profile else 'general',
            'preferred_ai_provider': profile.preferred_ai_provider if profile else 'openai',
            'native_language': profile.native_language if profile else 'es',
            'target_language': profile.target_language if profile else 'en',
            # Future settings
            'notifications_enabled': True,
            'reminder_time': '09:00',
        })
    
    def patch(self, request):
        user = request.user
        profile = getattr(user, 'learning_profile', None)
        
        if not profile:
            return Response(
                {'error': 'Learning profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Allowed fields to update
        allowed_fields = [
            'daily_goal_minutes', 'learning_goal', 'preferred_ai_provider',
            'native_language', 'target_language'
        ]
        
        updated_fields = []
        for field in allowed_fields:
            if field in request.data:
                value = request.data[field]
                
                # Validation
                if field == 'daily_goal_minutes':
                    value = max(5, min(120, int(value)))
                
                setattr(profile, field, value)
                updated_fields.append(field)
        
        if updated_fields:
            profile.save(update_fields=updated_fields)
        
        return Response({
            'message': 'Settings updated',
            'updated_fields': updated_fields,
            'daily_goal_minutes': profile.daily_goal_minutes,
            'learning_goal': profile.learning_goal,
            'preferred_ai_provider': profile.preferred_ai_provider,
        })
