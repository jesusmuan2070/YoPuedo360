"""
Streak Service - Manages user streaks and daily activity bonuses.
"""
from typing import Dict, Optional
from datetime import date, timedelta
from django.conf import settings
from django.utils import timezone

from apps.users.services.xp_service import XPService
from apps.users.utils.timezone import get_user_today, get_user_yesterday


class StreakService:
    """
    Service to manage user streaks and award bonuses.
    
    A streak is maintained when user has >= 5 minutes of activity per day.
    
    Usage:
        from apps.users.services.streak_service import StreakService
        
        # Process daily streaks for all users (run via cron)
        StreakService.process_daily_streaks()
        
        # Check if user was active today
        StreakService.was_active_today(user)
    """
    
    @staticmethod
    def get_min_activity_minutes() -> int:
        """Get minimum minutes required to count as active day."""
        config = settings.LEARNING_CONFIG.get('streak', {})
        return config.get('min_activity_minutes', 5)
    
    @staticmethod
    def get_activity_for_date(user, target_date: date) -> Optional['DailyActivity']:
        """Get DailyActivity record for a specific date."""
        from apps.users.models import DailyActivity
        
        return DailyActivity.objects.filter(
            user=user,
            date=target_date
        ).first()
    
    @classmethod
    def was_active_on_date(cls, user, target_date: date) -> bool:
        """Check if user met minimum activity requirement on a date."""
        activity = cls.get_activity_for_date(user, target_date)
        if not activity:
            return False
        
        min_minutes = cls.get_min_activity_minutes()
        return activity.minutes_studied >= min_minutes
    
    @classmethod
    def was_active_today(cls, user) -> bool:
        """Check if user met minimum activity requirement today (in user's timezone)."""
        return cls.was_active_on_date(user, get_user_today(user))
    
    @classmethod
    def was_active_yesterday(cls, user) -> bool:
        """Check if user met minimum activity requirement yesterday (in user's timezone)."""
        return cls.was_active_on_date(user, get_user_yesterday(user))
    
    @classmethod
    def update_streak(cls, user) -> Dict:
        """
        DEPRECATED: This method was designed for a daily cron job.
        
        Streak is now updated in real-time by DailyActivityService.record_activity()
        when the user crosses the 5-minute threshold.
        
        Keeping this method for reference/rollback but it should NOT be called.
        
        ---
        Original docstring:
        Update user's streak based on yesterday's activity.
        Called by daily cron job.
        
        Returns:
            Dict with streak update details
        """
        import warnings
        warnings.warn(
            "update_streak() is deprecated. Streak is now updated real-time in DailyActivityService.",
            DeprecationWarning
        )
        
        profile = getattr(user, 'learning_profile', None)
        if not profile:
            return {'error': 'No learning profile', 'updated': False}
        
        yesterday = timezone.now().date() - timedelta(days=1)
        was_active = cls.was_active_on_date(user, yesterday)
        
        old_streak = profile.streak_days
        
        if was_active:
            # Increment streak
            profile.streak_days += 1
            
            # Update longest streak if new record
            if profile.streak_days > profile.longest_streak:
                profile.longest_streak = profile.streak_days
            
            profile.save(update_fields=['streak_days', 'longest_streak'])
            
            return {
                'updated': True,
                'action': 'incremented',
                'old_streak': old_streak,
                'new_streak': profile.streak_days,
                'longest_streak': profile.longest_streak,
            }
        else:
            # Reset streak - but first check for streak freeze
            # (streak freeze feature can be added later)
            profile.streak_days = 0
            profile.save(update_fields=['streak_days'])
            
            return {
                'updated': True,
                'action': 'reset',
                'old_streak': old_streak,
                'new_streak': 0,
            }
    
    @classmethod
    def award_daily_bonuses(cls, user) -> Dict:
        """
        Award bonuses for daily activity.
        Called when user completes their daily goal.
        
        Returns:
            Dict with bonus details
        """
        profile = getattr(user, 'learning_profile', None)
        if not profile:
            return {'error': 'No learning profile'}
        
        today = timezone.now().date()
        activity = cls.get_activity_for_date(user, today)
        
        if not activity:
            return {'bonuses_awarded': False, 'reason': 'No activity today'}
        
        bonuses = []
        
        # Daily goal bonus
        if activity.daily_goal_met and not getattr(activity, '_daily_goal_bonus_awarded', False):
            result = XPService.award_daily_goal_bonus(user)
            bonuses.append({
                'type': 'daily_goal',
                'xp': result.get('xp_awarded', 0)
            })
        
        # Streak bonus (if streak is active)
        if profile.streak_days > 0:
            result = XPService.award_streak_bonus(user, profile.streak_days)
            bonuses.append({
                'type': 'streak',
                'streak_days': profile.streak_days,
                'xp': result.get('xp_awarded', 0)
            })
        
        return {
            'bonuses_awarded': len(bonuses) > 0,
            'bonuses': bonuses,
            'total_bonus_xp': sum(b['xp'] for b in bonuses)
        }
    
    @classmethod
    def process_daily_streaks(cls) -> Dict:
        """
        DEPRECATED: This cron job is no longer needed.
        
        Streak is now updated in real-time by DailyActivityService.record_activity()
        when each user crosses the 5-minute threshold.
        
        Keeping this method for reference/rollback but it should NOT be scheduled.
        
        ---
        Original docstring:
        Process streaks for all users. Run daily via cron.
        
        Returns:
            Summary of processed users
        """
        import warnings
        warnings.warn(
            "process_daily_streaks() is deprecated. Streaks are now updated real-time.",
            DeprecationWarning
        )
        
        from apps.users.models import User
        
        users = User.objects.all()
        
        results = {
            'processed': 0,
            'incremented': 0,
            'reset': 0,
            'errors': 0,
        }
        
        for user in users:
            try:
                result = cls.update_streak(user)
                results['processed'] += 1
                
                if result.get('action') == 'incremented':
                    results['incremented'] += 1
                elif result.get('action') == 'reset':
                    results['reset'] += 1
                    
            except Exception as e:
                results['errors'] += 1
        
        return results
