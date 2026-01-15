"""
Recommendation Models
"""

from django.db import models
from django.conf import settings


class RecommendationLog(models.Model):
    """
    Logs recommendation requests for analytics and debugging.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recommendation_logs'
    )
    
    # What was recommended
    scenario_ids = models.JSONField(default=list)
    total_available = models.IntegerField(default=0)
    
    # User profile at time of recommendation
    user_level = models.CharField(max_length=10)
    user_goals = models.JSONField(default=dict)
    user_interests = models.JSONField(default=dict)
    
    # Filters applied
    filters_applied = models.JSONField(default=list)
    
    # Timing
    processing_time_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'recommendation_logs'
        ordering = ['-created_at']
        verbose_name = 'Recommendation Log'
        verbose_name_plural = 'Recommendation Logs'
    
    def __str__(self):
        return f"Rec for {self.user} at {self.created_at}"


class UserOrderedScenarios(models.Model):
    """
    Stores ARIA's ordered scenario list per user.
    Generated once after onboarding, regenerated when profile changes.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='ordered_scenarios'
    )
    
    # Ordered list of scenario IDs from OpenAI ranking
    scenario_order = models.JSONField(default=list)  # [id1, id2, id3, ...]
    
    # Metadata
    user_level = models.CharField(max_length=2, default='A1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Track what profile data was used (to detect changes)
    profile_hash = models.CharField(max_length=64, blank=True)
    
    class Meta:
        db_table = 'user_ordered_scenarios'
        verbose_name = 'User Ordered Scenarios'
        verbose_name_plural = 'User Ordered Scenarios'
    
    def __str__(self):
        return f"Scenarios for {self.user.username} ({len(self.scenario_order)} ordered)"
    
    def invalidate(self):
        """Clear order to force regeneration on next request."""
        self.scenario_order = []
        self.profile_hash = ''
        self.save()


