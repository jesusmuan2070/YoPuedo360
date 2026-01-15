"""
Onboarding models for YoPuedo360.
Defines the onboarding steps and VAK assessment questions.
"""

from django.db import models
from django.conf import settings


class OnboardingStep(models.Model):
    """
    Defines each step in the onboarding flow.
    Steps are configurable and can be reordered.
    """
    
    class StepType(models.TextChoices):
        WELCOME = 'welcome', 'Welcome'
        LANGUAGE_SELECT = 'language_select', 'Language Selection'
        GOAL_SELECT = 'goal_select', 'Goal Setting'
        LEVEL_SELECT = 'level_select', 'Level Selection'
        STYLE_ASSESSMENT = 'style_assessment', 'Learning Style Assessment'
        TIME_COMMITMENT = 'time_commitment', 'Time Commitment'
        AVATAR_CREATE = 'avatar_create', 'Avatar Creation'
        WORLD_PREVIEW = 'world_preview', 'World Preview'
        FIRST_LESSON = 'first_lesson', 'First Lesson'
    
    order = models.PositiveIntegerField(unique=True)
    step_type = models.CharField(max_length=30, choices=StepType.choices)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # React component to render
    component_name = models.CharField(max_length=100)
    
    # Configuration
    is_required = models.BooleanField(default=True)
    is_skippable = models.BooleanField(default=False)
    
    # UI customization
    icon = models.CharField(max_length=10, default='📝')
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'onboarding_steps'
        ordering = ['order']
        verbose_name = 'Onboarding Step'
        verbose_name_plural = 'Onboarding Steps'
    
    def __str__(self):
        return f"{self.order}. {self.title}"


class VAKAssessmentQuestion(models.Model):
    """
    Questions for the Visual-Auditory-Kinesthetic learning style assessment.
    Each question has 3 options representing each learning channel.
    """
    
    order = models.PositiveIntegerField()
    question_text = models.TextField()
    
    # Options and their channel association
    visual_option = models.CharField(max_length=255)
    auditory_option = models.CharField(max_length=255)
    kinesthetic_option = models.CharField(max_length=255)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'vak_assessment_questions'
        ordering = ['order']
        verbose_name = 'VAK Assessment Question'
        verbose_name_plural = 'VAK Assessment Questions'
    
    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}..."


class UserOnboardingProgress(models.Model):
    """
    Tracks user's progress through onboarding.
    """
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='onboarding_progress'
    )
    
    current_step = models.PositiveIntegerField(default=1)
    completed_steps = models.JSONField(default=list)
    
    # Collected data during onboarding (before profile creation)
    collected_data = models.JSONField(default=dict)
    
    # VAK assessment answers
    vak_answers = models.JSONField(default=list)
    
    # Status
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_onboarding_progress'
        verbose_name = 'User Onboarding Progress'
        verbose_name_plural = 'User Onboarding Progress'
    
    def __str__(self):
        return f"{self.user.username} - Step {self.current_step}"
