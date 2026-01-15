"""
Base Exercise Model - Abstract base for all exercise types
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ExerciseBase(models.Model):
    """
    Abstract base model for all exercise types.
    Contains common fields shared by all exercises.
    """
    LEVEL_CHOICES = [
        ('A1', 'A1'), ('A2', 'A2'),
        ('B1', 'B1'), ('B2', 'B2'),
        ('C1', 'C1'), ('C2', 'C2'),
    ]
    
    DIFFICULTY_CHOICES = [
        (1, 'Muy fácil'),
        (2, 'Fácil'),
        (3, 'Normal'),
        (4, 'Difícil'),
        (5, 'Muy difícil'),
    ]
    
    # Relaciones
    milestone = models.ForeignKey(
        'memory_palace.Milestone',
        on_delete=models.CASCADE,
        related_name='%(class)s_exercises',
        null=True, blank=True
    )
    grammar_topic = models.ForeignKey(
        'content.GrammarTopic',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='%(class)s_exercises'
    )
    
    # Metadatos
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, db_index=True)
    difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES, default=3)
    
    # Recompensas
    xp_reward = models.PositiveIntegerField(default=10)
    
    # Estado
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Instrucciones
    instructions = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Instrucciones para el usuario, ej: 'Ordena las palabras'"
    )
    
    class Meta:
        abstract = True
        ordering = ['level', 'difficulty']
    
    def check_answer(self, user_answer):
        """
        Override in subclasses to validate user's answer.
        Returns: (is_correct: bool, feedback: str)
        """
        raise NotImplementedError("Subclasses must implement check_answer()")
    
    def get_display_data(self):
        """
        Override in subclasses to return data for frontend display.
        """
        raise NotImplementedError("Subclasses must implement get_display_data()")


class ExerciseAttempt(models.Model):
    """
    Tracks user attempts at exercises.
    Generic relation to any exercise type.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_attempts')
    
    # Generic reference to any exercise type
    exercise_type = models.CharField(max_length=50)  # 'word_order', 'fill_blank', etc.
    exercise_id = models.PositiveIntegerField()
    
    # Attempt data
    user_answer = models.JSONField()  # What the user submitted
    is_correct = models.BooleanField()
    
    # Timing
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(auto_now_add=True)
    time_spent_seconds = models.PositiveIntegerField(default=0)
    
    # Rewards
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
    def record_attempt(cls, user, exercise, user_answer, is_correct, started_at):
        """Helper to record an attempt"""
        time_spent = int((timezone.now() - started_at).total_seconds())
        xp = exercise.xp_reward if is_correct else 0
        
        return cls.objects.create(
            user=user,
            exercise_type=exercise.__class__.__name__.lower().replace('exercise', ''),
            exercise_id=exercise.id,
            user_answer=user_answer,
            is_correct=is_correct,
            started_at=started_at,
            time_spent_seconds=time_spent,
            xp_earned=xp,
        )
