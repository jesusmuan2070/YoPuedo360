"""
XP Service - Centralized XP calculation with CEFR multipliers.
All XP awards should go through this service.
"""
from typing import Dict, Optional
from django.conf import settings


class XPService:
    """
    Centralized XP calculation service.
    
    Usage:
        from apps.users.services.xp_service import XPService
        
        # Award XP for exercise
        result = XPService.award_exercise_xp(user, score=85, cefr_level='B1')
        
        # Award XP for learned word
        result = XPService.award_word_learned_xp(user, cefr_level='A2')
    """
    
    @staticmethod
    def get_config() -> Dict:
        """Get XP configuration from settings."""
        return settings.LEARNING_CONFIG
    
    @staticmethod
    def get_cefr_multiplier(cefr_level: str) -> float:
        """Get multiplier for a CEFR level."""
        multipliers = XPService.get_config().get('cefr_multipliers', {})
        return multipliers.get(cefr_level.upper(), 1.0)
    
    @staticmethod
    def get_base_xp(activity_type: str) -> int:
        """Get base XP for an activity type."""
        xp_base = XPService.get_config().get('xp_base', {})
        return xp_base.get(activity_type, 0)
    
    @staticmethod
    def calculate_xp(activity_type: str, cefr_level: str = 'A1', **kwargs) -> int:
        """
        Calculate XP for an activity with CEFR multiplier.
        
        Args:
            activity_type: Type of activity (exercise_complete, word_learned, etc.)
            cefr_level: CEFR level of the content (A1-C2)
            **kwargs: Additional params (e.g., score for exercises)
            
        Returns:
            Final XP amount (integer)
        """
        base_xp = XPService.get_base_xp(activity_type)
        multiplier = XPService.get_cefr_multiplier(cefr_level)
        
        # Special case: exercise score bonus
        if activity_type == 'exercise_complete' and 'score' in kwargs:
            score = kwargs['score']  # 0-100
            score_bonus = int(score * 0.4)  # 0-40 XP extra
            base_xp += score_bonus
        
        return int(base_xp * multiplier)
    
    @staticmethod
    def award_xp(user, amount: int, reason: str = '') -> Dict:
        """
        Award XP to a user and update their profile.
        
        Args:
            user: User instance
            amount: XP amount to award
            reason: Optional reason for logging
            
        Returns:
            Dict with new_total_xp, current_level, leveled_up
        """
        profile = getattr(user, 'learning_profile', None)
        if not profile:
            return {'error': 'No learning profile found'}
        
        result = profile.add_xp(amount)
        result['xp_awarded'] = amount
        result['reason'] = reason
        
        return result
    
    # ==========================================
    # Activity-specific award methods
    # ==========================================
    
    @classmethod
    def award_exercise_xp(cls, user, score: float, cefr_level: str = 'A1') -> Dict:
        """
        Award XP for completing an exercise.
        
        Args:
            user: User instance
            score: Score from 0-100
            cefr_level: CEFR level of the exercise content
            
        Returns:
            XP award result dict
        """
        xp = cls.calculate_xp('exercise_complete', cefr_level, score=score)
        return cls.award_xp(user, xp, f'Exercise completed (score={score}, level={cefr_level})')
    
    @classmethod
    def award_word_learned_xp(cls, user, cefr_level: str = 'A1') -> Dict:
        """Award XP when a word reaches 'learned' status in SRS."""
        xp = cls.calculate_xp('word_learned', cefr_level)
        return cls.award_xp(user, xp, f'Word learned (level={cefr_level})')
    
    @classmethod
    def award_word_reviewed_xp(cls, user, cefr_level: str = 'A1') -> Dict:
        """Award XP for a successful SRS review."""
        xp = cls.calculate_xp('word_reviewed', cefr_level)
        return cls.award_xp(user, xp, f'Word reviewed (level={cefr_level})')
    
    @classmethod
    def award_grammar_learned_xp(cls, user, cefr_level: str = 'A1') -> Dict:
        """Award XP when a grammar unit is mastered."""
        xp = cls.calculate_xp('grammar_learned', cefr_level)
        return cls.award_xp(user, xp, f'Grammar learned (level={cefr_level})')
    
    @classmethod
    def award_milestone_complete_xp(cls, user, cefr_level: str = 'A1') -> Dict:
        """Award XP for completing a milestone."""
        xp = cls.calculate_xp('milestone_complete', cefr_level)
        return cls.award_xp(user, xp, f'Milestone completed (level={cefr_level})')
    
    @classmethod
    def award_daily_goal_bonus(cls, user) -> Dict:
        """Award bonus XP for meeting daily goal (no CEFR multiplier)."""
        xp = cls.get_base_xp('daily_goal_bonus')
        return cls.award_xp(user, xp, 'Daily goal achieved')
    
    @classmethod
    def award_streak_bonus(cls, user, streak_days: int) -> Dict:
        """Award streak bonus XP (no CEFR multiplier)."""
        base = cls.get_base_xp('streak_bonus_per_day')
        xp = base * streak_days
        return cls.award_xp(user, xp, f'Streak bonus ({streak_days} days)')
