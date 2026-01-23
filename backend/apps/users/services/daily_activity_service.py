"""
Daily Activity Service - Tracks study time and handles daily goal completion.
"""
from typing import Dict, Optional
from datetime import date
from django.utils import timezone

from apps.users.services.xp_service import XPService


class DailyActivityService:
    """
    Service to track daily study activity and award bonuses.
    
    Usage:
        from apps.users.services.daily_activity_service import DailyActivityService
        
        # Record activity after completing an exercise
        result = DailyActivityService.record_activity(user, minutes=5)
        
        if result['just_completed_goal']:
            # Show celebration UI! 🎉
    """
    
    @staticmethod
    def get_or_create_today(user) -> 'DailyActivity':
        """Get or create DailyActivity record for today."""
        from apps.users.models import DailyActivity
        
        today = timezone.now().date()
        activity, created = DailyActivity.objects.get_or_create(
            user=user,
            date=today,
            defaults={'minutes_studied': 0}
        )
        return activity
    
    @staticmethod
    def get_daily_goal(user) -> int:
        """Get user's daily goal in minutes."""
        profile = getattr(user, 'learning_profile', None)
        if profile:
            return profile.daily_goal_minutes
        return 15  # Default
    
    @classmethod
    def record_activity(cls, user, minutes: int, xp_earned: int = 0) -> Dict:
        """
        Record study activity and check if daily goal is met.
        
        Args:
            user: User instance
            minutes: Minutes studied in this session
            xp_earned: XP earned in this session (for tracking)
            
        Returns:
            Dict with activity status and celebration flag
        """
        activity = cls.get_or_create_today(user)
        goal = cls.get_daily_goal(user)
        
        # Track previous state
        old_minutes = activity.minutes_studied
        old_goal_met = activity.daily_goal_met
        
        # Update activity
        activity.minutes_studied += minutes
        activity.xp_earned += xp_earned
        
        # Check if just completed daily goal
        just_completed_goal = False
        bonus_xp = 0
        
        if activity.minutes_studied >= goal and not old_goal_met:
            activity.daily_goal_met = True
            just_completed_goal = True
            
            # Award daily goal bonus XP
            result = XPService.award_daily_goal_bonus(user)
            bonus_xp = result.get('xp_awarded', 0)
        
        activity.save()
        
        return {
            'date': str(activity.date),
            'minutes_studied': activity.minutes_studied,
            'daily_goal': goal,
            'daily_goal_met': activity.daily_goal_met,
            'just_completed_goal': just_completed_goal,  # 🎉 For celebration UI
            'bonus_xp_awarded': bonus_xp,
            'progress_percent': min(100, int((activity.minutes_studied / goal) * 100)),
        }
    
    @classmethod
    def record_exercise_completion(cls, user, time_spent_seconds: int, xp_earned: int) -> Dict:
        """
        Convenience method to record after exercise completion.
        
        Args:
            user: User instance
            time_spent_seconds: Time spent on exercise
            xp_earned: XP earned from exercise
        """
        minutes = max(1, time_spent_seconds // 60)  # At least 1 minute
        return cls.record_activity(user, minutes=minutes, xp_earned=xp_earned)
    
    @classmethod
    def record_lesson_completion(cls, user, time_spent_seconds: int, xp_earned: int) -> Dict:
        """
        Convenience method to record after lesson completion.
        """
        minutes = max(1, time_spent_seconds // 60)
        return cls.record_activity(user, minutes=minutes, xp_earned=xp_earned)
    
    @classmethod
    def get_today_stats(cls, user) -> Dict:
        """Get today's activity stats without modifying."""
        activity = cls.get_or_create_today(user)
        goal = cls.get_daily_goal(user)
        
        return {
            'date': str(activity.date),
            'minutes_studied': activity.minutes_studied,
            'daily_goal': goal,
            'daily_goal_met': activity.daily_goal_met,
            'xp_earned_today': activity.xp_earned,
            'progress_percent': min(100, int((activity.minutes_studied / goal) * 100)),
            'minutes_remaining': max(0, goal - activity.minutes_studied),
        }
