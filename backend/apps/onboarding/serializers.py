"""
Serializers for onboarding API.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.users.models import LearningProfile
from .models import OnboardingStep, VAKAssessmentQuestion, UserOnboardingProgress


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration during onboarding."""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match.'
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        # Create onboarding progress
        UserOnboardingProgress.objects.create(user=user)
        return user


class OnboardingStepSerializer(serializers.ModelSerializer):
    """Serializer for onboarding steps."""
    
    class Meta:
        model = OnboardingStep
        fields = [
            'order', 'step_type', 'title', 'description',
            'component_name', 'is_required', 'is_skippable', 'icon'
        ]


class VAKAssessmentQuestionSerializer(serializers.ModelSerializer):
    """Serializer for VAK assessment questions."""
    
    options = serializers.SerializerMethodField()
    
    class Meta:
        model = VAKAssessmentQuestion
        fields = ['order', 'question_text', 'options']
    
    def get_options(self, obj):
        return [
            {'id': 'visual', 'text': obj.visual_option},
            {'id': 'auditory', 'text': obj.auditory_option},
            {'id': 'kinesthetic', 'text': obj.kinesthetic_option},
        ]


class VAKAnswerSerializer(serializers.Serializer):
    """Serializer for submitting VAK answers."""
    
    question_order = serializers.IntegerField()
    answer = serializers.ChoiceField(choices=['visual', 'auditory', 'kinesthetic'])


class LanguageSelectionSerializer(serializers.Serializer):
    """Serializer for language selection step."""
    
    native_language = serializers.CharField(max_length=10)
    target_language = serializers.CharField(max_length=10)


class GoalSelectionSerializer(serializers.Serializer):
    """Serializer for goal selection step."""
    
    GOAL_CHOICES = [
        ('travel', 'Travel'),
        ('work', 'Work/Career'),
        ('certification', 'Certification'),
        ('personal', 'Personal Growth'),
        ('general', 'General'),
    ]
    learning_goal = serializers.ChoiceField(choices=GOAL_CHOICES)


class LevelSelectionSerializer(serializers.Serializer):
    """Serializer for level selection step."""
    
    LEVEL_CHOICES = [
        (1, 'Complete Beginner'),
        (2, 'Know Some Basics'),
        (3, 'Simple Conversations'),
        (4, 'Intermediate'),
        (5, 'Test My Level'),  # Triggers placement test
    ]
    initial_level = serializers.ChoiceField(choices=LEVEL_CHOICES)


class TimeCommitmentSerializer(serializers.Serializer):
    """Serializer for time commitment step."""
    
    TIME_CHOICES = [
        (5, 'Casual - 5 min'),
        (15, 'Regular - 15 min'),
        (30, 'Serious - 30 min'),
        (60, 'Intensive - 60 min'),
    ]
    daily_goal_minutes = serializers.ChoiceField(choices=TIME_CHOICES)


class OnboardingStepCompleteSerializer(serializers.Serializer):
    """Generic serializer for completing an onboarding step."""
    
    step_type = serializers.CharField()
    data = serializers.DictField()


class UserOnboardingProgressSerializer(serializers.ModelSerializer):
    """Serializer for user's onboarding progress."""
    
    class Meta:
        model = UserOnboardingProgress
        fields = [
            'current_step', 'completed_steps', 'collected_data',
            'is_completed', 'started_at', 'updated_at'
        ]
        read_only_fields = fields


class VAKResultSerializer(serializers.Serializer):
    """Serializer for VAK assessment results."""
    
    visual_score = serializers.IntegerField()
    auditory_score = serializers.IntegerField()
    kinesthetic_score = serializers.IntegerField()
    primary_style = serializers.CharField()
    secondary_style = serializers.CharField(allow_null=True)


class OnboardingCompleteSerializer(serializers.Serializer):
    """Serializer for completing full onboarding."""
    
    # All collected data
    native_language = serializers.CharField()
    target_language = serializers.CharField()
    learning_goal = serializers.CharField()
    initial_level = serializers.IntegerField()
    daily_goal_minutes = serializers.IntegerField()
    vak_answers = serializers.ListField(child=VAKAnswerSerializer())
    avatar_name = serializers.CharField(max_length=50, required=False)
