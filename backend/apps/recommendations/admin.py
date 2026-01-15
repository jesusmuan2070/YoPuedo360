"""
Recommendation Admin
"""

from django.contrib import admin
from .models import RecommendationLog


@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_level', 'total_available', 'processing_time_ms', 'created_at']
    list_filter = ['user_level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['user', 'scenario_ids', 'user_goals', 'user_interests', 'filters_applied', 'created_at']
