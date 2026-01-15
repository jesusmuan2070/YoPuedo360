"""
Milestone Progress - Track user progress through milestones and exercises
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class UserMilestoneProgress(models.Model):
    """
    Tracks user progress through milestones.
    Determines which milestones are completed vs pending.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='milestone_progress'
    )
    milestone = models.ForeignKey(
        'memory_palace.Milestone',
        on_delete=models.CASCADE,
        related_name='user_progress'
    )
    
    # Status
    STATUS_CHOICES = [
        ('not_started', 'No iniciado'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    # Progress tracking
    progress_percent = models.PositiveIntegerField(default=0)  # 0-100
    exercises_completed = models.PositiveIntegerField(default=0)
    exercises_total = models.PositiveIntegerField(default=0)
    
    # Scores
    best_score = models.PositiveIntegerField(default=0)  # 0-100
    last_score = models.PositiveIntegerField(default=0)
    attempts = models.PositiveIntegerField(default=0)
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    # Time spent
    total_time_seconds = models.PositiveIntegerField(default=0)
    
    # XP earned from this milestone
    xp_earned = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'milestone']
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'milestone']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.milestone} ({self.status})"
    
    def start(self):
        """Mark milestone as started"""
        if self.status == 'not_started':
            self.status = 'in_progress'
            self.started_at = timezone.now()
            self.save()
    
    def complete(self, score=100, time_spent=0):
        """Mark milestone as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.progress_percent = 100
        self.last_score = score
        self.best_score = max(self.best_score, score)
        self.attempts += 1
        self.total_time_seconds += time_spent
        
        # Award XP (from milestone)
        if self.xp_earned == 0:  # First completion
            self.xp_earned = self.milestone.xp_reward or 10
        
        self.save()
    
    def update_progress(self, exercises_done, exercises_total):
        """Update progress percentage"""
        self.exercises_completed = exercises_done
        self.exercises_total = exercises_total
        if exercises_total > 0:
            self.progress_percent = int((exercises_done / exercises_total) * 100)
        self.save()
    
    @classmethod
    def get_completed_milestones(cls, user, scenario=None):
        """Get list of completed milestone IDs for a user"""
        qs = cls.objects.filter(user=user, status='completed')
        if scenario:
            qs = qs.filter(milestone__scenario=scenario)
        return qs.values_list('milestone_id', flat=True)
    
    @classmethod
    def get_pending_milestones(cls, user, scenario):
        """Get milestones not yet completed in a scenario"""
        from apps.memory_palace.models import Milestone
        
        completed = cls.get_completed_milestones(user, scenario)
        return Milestone.objects.filter(
            scenario=scenario
        ).exclude(id__in=completed).order_by('order')
    
    @classmethod
    def get_next_milestone(cls, user, scenario):
        """Get next milestone to work on"""
        pending = cls.get_pending_milestones(user, scenario)
        return pending.first()
    
    @classmethod
    def get_scenario_progress(cls, user, scenario):
        """Get progress summary for a scenario"""
        from apps.memory_palace.models import Milestone
        
        total_milestones = Milestone.objects.filter(scenario=scenario).count()
        completed = cls.objects.filter(
            user=user,
            milestone__scenario=scenario,
            status='completed'
        ).count()
        in_progress = cls.objects.filter(
            user=user,
            milestone__scenario=scenario,
            status='in_progress'
        ).count()
        
        return {
            'total': total_milestones,
            'completed': completed,
            'in_progress': in_progress,
            'not_started': total_milestones - completed - in_progress,
            'percent': int((completed / total_milestones * 100)) if total_milestones > 0 else 0,
        }


class UserExerciseAttempt(models.Model):
    """
    Records individual exercise attempts within a milestone.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_attempts_progress')
    milestone_progress = models.ForeignKey(
        UserMilestoneProgress,
        on_delete=models.CASCADE,
        related_name='exercise_attempts',
        null=True, blank=True
    )
    
    # Exercise reference (generic - works with any exercise type)
    exercise_type = models.CharField(max_length=50)  # 'word_order', 'fill_blank', etc.
    exercise_id = models.PositiveIntegerField()
    
    # Attempt data
    user_answer = models.JSONField()
    is_correct = models.BooleanField()
    
    # Score (for partial credit)
    score = models.PositiveIntegerField(default=0)  # 0-100
    
    # Timing
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(auto_now_add=True)
    time_spent_seconds = models.PositiveIntegerField(default=0)
    
    # Hints/Help used
    hints_used = models.PositiveIntegerField(default=0)
    
    # XP earned
    xp_earned = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-completed_at']
        indexes = [
            models.Index(fields=['user', 'exercise_type', 'exercise_id']),
            models.Index(fields=['user', 'completed_at']),
        ]
    
    def __str__(self):
        status = "✅" if self.is_correct else "❌"
        return f"{self.user.username} - {self.exercise_type} #{self.exercise_id} {status}"
    
    @classmethod
    def record(cls, user, exercise, user_answer, is_correct, started_at, 
               milestone_progress=None, hints_used=0):
        """Helper to record an attempt"""
        time_spent = int((timezone.now() - started_at).total_seconds())
        score = 100 if is_correct else 0
        xp = exercise.xp_reward if is_correct else 0
        
        attempt = cls.objects.create(
            user=user,
            milestone_progress=milestone_progress,
            exercise_type=exercise.__class__.__name__.lower().replace('exercise', ''),
            exercise_id=exercise.id,
            user_answer=user_answer,
            is_correct=is_correct,
            score=score,
            started_at=started_at,
            time_spent_seconds=time_spent,
            hints_used=hints_used,
            xp_earned=xp,
        )
        
        # Update milestone progress if linked
        if milestone_progress:
            milestone_progress.exercises_completed += 1 if is_correct else 0
            milestone_progress.save()
        
        return attempt
