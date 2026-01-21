"""
URL Configuration for Intents API
"""

from django.urls import path
from . import views

app_name = 'intents'

urlpatterns = [
    # Scenarios
    path('scenarios/', views.get_scenarios, name='scenarios-list'),
    path('scenarios/<slug:slug>/progress/', views.get_scenario_progress, name='scenario-progress'),
    
    # Milestones
    path('milestones/<int:milestone_id>/start/', views.start_milestone, name='milestone-start'),
    path('milestones/<int:milestone_id>/content/', views.get_milestone_content, name='milestone-content'),
    
    # Intents
    path('intents/<int:intent_id>/complete/', views.complete_intent, name='intent-complete'),
    
    # User progress
    path('progress/', views.get_user_progress, name='user-progress'),
]
