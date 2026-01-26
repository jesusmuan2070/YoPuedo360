"""
User models for YoPuedo360.
Custom User model with learning profile integration.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for YoPuedo360 platform.
    Extends Django's AbstractUser with learning-specific fields.
    """
    
    # OAuth connections
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    apple_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    
    # Profile
    avatar_url = models.URLField(blank=True, null=True)
    
    # Timestamps
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email or self.username


class LearningProfile(models.Model):
    """
    User's learning preferences and assessment results.
    Created during onboarding and updated as user progresses.
    """
    
    class LearningChannel(models.TextChoices):
        VISUAL = 'visual', 'Visual'
        AUDITORY = 'auditory', 'Auditory'
        KINESTHETIC = 'kinesthetic', 'Kinesthetic'
    
    class LearningGoal(models.TextChoices):
        TRAVEL = 'travel', 'Travel'
        WORK = 'work', 'Work/Career'
        CERTIFICATION = 'certification', 'Certification'
        PERSONAL = 'personal', 'Personal Growth'
        GENERAL = 'general', 'General'
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='learning_profile'
    )
    
    # Language settings
    native_language = models.CharField(max_length=10, default='es')  # ISO code
    target_language = models.CharField(max_length=10, default='en')  # ISO code
    
    # Learning goals
    learning_goal = models.CharField(
        max_length=20,
        choices=LearningGoal.choices,
        default=LearningGoal.GENERAL
    )
    daily_goal_minutes = models.PositiveIntegerField(default=15)
    
    # Learning style assessment results (0-100 for each)
    visual_score = models.PositiveIntegerField(default=33)
    auditory_score = models.PositiveIntegerField(default=33)
    kinesthetic_score = models.PositiveIntegerField(default=34)
    
    # Derived primary style
    primary_style = models.CharField(
        max_length=20,
        choices=LearningChannel.choices,
        default=LearningChannel.VISUAL
    )
    
    # Current progress state
    current_level = models.PositiveIntegerField(default=1)  # 1-10
    total_xp = models.PositiveIntegerField(default=0)
    streak_days = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    
    # Memory Palace position
    current_world_id = models.PositiveIntegerField(null=True, blank=True)
    current_room_id = models.PositiveIntegerField(null=True, blank=True)
    
    # AI preferences
    preferred_ai_provider = models.CharField(max_length=20, default='openai')
    
    # Onboarding status
    onboarding_completed = models.BooleanField(default=False)
    onboarding_step = models.PositiveIntegerField(default=0)
    
    # Timezone for correct streak calculation
    timezone = models.CharField(max_length=50, default='America/Mexico_City')
    
    # Last activity date (DATE not DATETIME - for streak logic)
    last_activity_date = models.DateField(null=True, blank=True)
    
    # 🆕 Recommendation Algorithm fields
    cefr_level = models.CharField(
        max_length=2, 
        default='A1',
        choices=[
            ('A1', 'A1'), ('A2', 'A2'),
            ('B1', 'B1'), ('B2', 'B2'),
            ('C1', 'C1'), ('C2', 'C2'),
        ]
    )
    
    # Goals con pesos (del onboarding)
    # Ejemplo: {"work": 0.6, "travel": 0.4}
    goals = models.JSONField(default=dict, blank=True)
    
    # Intereses personales (del onboarding)
    # Ejemplo: {"gaming": 0.8, "food": 0.5, "sports": 0.3}
    interests = models.JSONField(default=dict, blank=True)
    
    # Dominio de trabajo si la meta es "work"
    # Ejemplo: "tech", "sales", "health", "education", "creative"
    work_domain = models.CharField(max_length=30, blank=True)
    
    # 🆕 Campos para personalización por IA
    # Profesión específica (texto libre para que IA genere contenido)
    # Ejemplo: "Técnico reparador de celulares", "Neurocirujano", "Chef"
    profession = models.CharField(max_length=100, blank=True)
    
    # Hobbies/Deportes específicos (lista de texto libre)
    # Ejemplo: ["nadar", "soccer", "leer", "videojuegos"]
    hobbies = models.JSONField(default=list, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'learning_profiles'
        verbose_name = 'Learning Profile'
        verbose_name_plural = 'Learning Profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Learning Profile"
    
    def update_primary_style(self):
        """Update primary style based on VAK scores."""
        scores = {
            self.LearningChannel.VISUAL: self.visual_score,
            self.LearningChannel.AUDITORY: self.auditory_score,
            self.LearningChannel.KINESTHETIC: self.kinesthetic_score,
        }
        self.primary_style = max(scores, key=scores.get)
        self.save(update_fields=['primary_style'])
    
    def add_xp(self, amount: int) -> dict:
        """Add XP to user and check for level up."""
        self.total_xp += amount
        
        # Simple level calculation: level = 1 + (total_xp // 1000)
        new_level = 1 + (self.total_xp // 1000)
        leveled_up = new_level > self.current_level
        
        if leveled_up:
            self.current_level = min(new_level, 10)  # Max level 10
        
        self.save(update_fields=['total_xp', 'current_level'])
        
        return {
            'new_total_xp': self.total_xp,
            'current_level': self.current_level,
            'leveled_up': leveled_up,
        }


class DailyActivity(models.Model):
    """
    Daily activity tracking for streaks and analytics.
    One record per user per day.
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='daily_activities'
    )
    date = models.DateField()
    
    # Activity metrics
    minutes_studied = models.PositiveIntegerField(default=0)
    xp_earned = models.PositiveIntegerField(default=0)
    exercises_completed = models.PositiveIntegerField(default=0)
    lessons_completed = models.PositiveIntegerField(default=0)
    words_learned = models.PositiveIntegerField(default=0)
    words_reviewed = models.PositiveIntegerField(default=0)
    
    # Goal tracking
    daily_goal_met = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'daily_activities'
        unique_together = ['user', 'date']
        ordering = ['-date']
        verbose_name = 'Daily Activity'
        verbose_name_plural = 'Daily Activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
