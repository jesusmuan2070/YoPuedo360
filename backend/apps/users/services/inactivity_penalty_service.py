"""
Inactivity Penalty Service
Handles XP penalties for users who don't practice daily.
"""
from typing import Dict, Optional
from datetime import date, timedelta
from django.conf import settings
from django.utils import timezone


class InactivityPenaltyService:
    """
    Service to calculate and apply XP penalties for inactivity.
    
    Penalty schedule (configurable in settings):
    - Day 1 without activity: No penalty (grace period)
    - Day 2: -5 XP
    - Day 3: -10 XP
    - Day 4: -15 XP
    - Day 5+: -20 XP (max)
    
    Usage:
        from apps.users.services.inactivity_penalty_service import InactivityPenaltyService
        
        # Check and apply penalty for a user
        result = InactivityPenaltyService.check_and_apply_penalty(user)
    """
    
    @staticmethod
    def get_config() -> Dict:
        """Get penalty configuration from settings."""
        return settings.LEARNING_CONFIG
    
    @staticmethod
    def get_penalty_for_days(days_inactive: int) -> int:
        """
        Get XP penalty amount for given days of inactivity.
        
        Args:
            days_inactive: Number of consecutive days without activity
            
        Returns:
            XP penalty amount (positive integer)
        """
        if days_inactive <= 1:
            return 0  # Grace period
        
        config = InactivityPenaltyService.get_config()
        penalties = config.get('inactivity_penalties', {2: 5, 3: 10, 4: 15})
        max_penalty = config.get('max_daily_penalty', 20)
        
        return penalties.get(days_inactive, max_penalty)
    
    @staticmethod
    def get_days_inactive(user) -> int:
        """
        Calculate how many days the user has been inactive.
        
        Args:
            user: User instance
            
        Returns:
            Number of days since last activity (0 if active today)
        """
        from apps.users.models import DailyActivity
        
        today = timezone.now().date()
        
        # Find the most recent activity
        last_activity = DailyActivity.objects.filter(
            user=user,
            minutes_studied__gt=0  # Only count days with actual activity
        ).order_by('-date').first()
        
        if not last_activity:
            # No activity ever recorded - check profile creation date
            profile = getattr(user, 'learning_profile', None)
            if profile:
                days_since_creation = (today - profile.created_at.date()).days
                return days_since_creation
            return 0
        
        days_inactive = (today - last_activity.date).days
        return days_inactive
    
    @staticmethod
    def apply_penalty(user, penalty_amount: int, days_inactive: int) -> Dict:
        """
        Apply XP penalty to user's profile.
        
        Args:
            user: User instance
            penalty_amount: XP to subtract
            days_inactive: For logging purposes
            
        Returns:
            Dict with penalty details
        """
        profile = getattr(user, 'learning_profile', None)
        if not profile:
            return {'error': 'No learning profile found', 'applied': False}
        
        old_xp = profile.total_xp
        
        # Apply penalty but never go below 0
        new_xp = max(0, profile.total_xp - penalty_amount)
        profile.total_xp = new_xp
        
        # IMPORTANT: Never reduce level, only XP
        # Level stays the same even if XP drops
        
        profile.save(update_fields=['total_xp'])
        
        return {
            'applied': True,
            'user_id': user.id,
            'username': user.username,
            'days_inactive': days_inactive,
            'penalty_amount': penalty_amount,
            'old_xp': old_xp,
            'new_xp': new_xp,
            'xp_lost': old_xp - new_xp,
            'level_unchanged': profile.current_level,  # Level never changes
        }
    
    @classmethod
    def check_and_apply_penalty(cls, user) -> Dict:
        """
        Check if user is inactive and apply penalty if needed.
        
        Args:
            user: User instance
            
        Returns:
            Dict with result (penalty applied or not)
        """
        days_inactive = cls.get_days_inactive(user)
        penalty = cls.get_penalty_for_days(days_inactive)
        
        if penalty == 0:
            return {
                'applied': False,
                'user_id': user.id,
                'days_inactive': days_inactive,
                'reason': 'No penalty (grace period or active)'
            }
        
        return cls.apply_penalty(user, penalty, days_inactive)
    
    @classmethod
    def get_inactive_users(cls, min_days: int = 2):
        """
        Get all users who have been inactive for at least min_days.
        
        Args:
            min_days: Minimum days of inactivity (default 2 for penalty)
            
        Returns:
            List of (user, days_inactive) tuples
        """
        from apps.users.models import User, DailyActivity
        
        today = timezone.now().date()
        cutoff_date = today - timedelta(days=min_days - 1)
        
        # Users with recent activity
        active_user_ids = DailyActivity.objects.filter(
            date__gte=cutoff_date,
            minutes_studied__gt=0
        ).values_list('user_id', flat=True).distinct()
        
        # All users without recent activity
        inactive_users = User.objects.exclude(id__in=active_user_ids)
        
        results = []
        for user in inactive_users:
            days = cls.get_days_inactive(user)
            if days >= min_days:
                results.append((user, days))
        
        return results
