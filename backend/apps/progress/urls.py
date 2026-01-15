"""
Progress API URLs
"""
from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    # Overall progress
    path('', views.my_progress, name='my_progress'),
    
    # Scenario progress
    path('scenario/<slug:scenario_slug>/', views.scenario_progress, name='scenario_progress'),
    path('scenario/<slug:scenario_slug>/pending/', views.pending_milestones, name='pending_milestones'),
    path('scenario/<slug:scenario_slug>/next/', views.next_milestone, name='next_milestone'),
    
    # Milestone actions
    path('milestone/<int:milestone_id>/', views.milestone_detail, name='milestone_detail'),
    path('start/', views.start_milestone, name='start_milestone'),
    path('complete/', views.complete_milestone, name='complete_milestone'),
]
