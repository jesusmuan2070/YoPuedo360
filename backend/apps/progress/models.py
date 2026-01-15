"""
Progress Models
Re-export from modular structure for Django migrations
"""
from .models import UserMilestoneProgress, UserExerciseAttempt

__all__ = [
    'UserMilestoneProgress',
    'UserExerciseAttempt',
]
