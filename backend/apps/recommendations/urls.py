"""
Recommendation URL routes
"""

from django.urls import path
from .views import RecommendedScenariosView, SimilarScenariosView

urlpatterns = [
    path('scenarios/', RecommendedScenariosView.as_view(), name='recommended-scenarios'),
    path('similar/<int:scenario_id>/', SimilarScenariosView.as_view(), name='similar-scenarios'),
]