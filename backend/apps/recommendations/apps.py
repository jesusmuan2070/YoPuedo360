"""
Recommendations App Configuration
"""

from django.apps import AppConfig


class RecommendationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.recommendations'
    verbose_name = 'ARIA - Recommendation Engine'
