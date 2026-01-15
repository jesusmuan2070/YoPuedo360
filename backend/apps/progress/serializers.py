"""
Progress Serializers
"""
from rest_framework import serializers
from .models import UserMilestoneProgress, UserExerciseAttempt


class UserMilestoneProgressSerializer(serializers.ModelSerializer):
    """Serializer for milestone progress"""
    milestone_name = serializers.CharField(source='milestone.name', read_only=True)
    milestone_level = serializers.CharField(source='milestone.level', read_only=True)
    scenario_name = serializers.CharField(source='milestone.scenario.name', read_only=True)
    scenario_slug = serializers.CharField(source='milestone.scenario.slug', read_only=True)
    
    class Meta:
        model = UserMilestoneProgress
        fields = [
            'id',
            'milestone',
            'milestone_name',
            'milestone_level',
            'scenario_name',
            'scenario_slug',
            'status',
            'progress_percent',
            'exercises_completed',
            'exercises_total',
            'best_score',
            'last_score',
            'attempts',
            'xp_earned',
            'started_at',
            'completed_at',
            'last_activity',
            'total_time_seconds',
        ]
        read_only_fields = ['id', 'xp_earned', 'started_at', 'completed_at', 'last_activity']


class ScenarioProgressSerializer(serializers.Serializer):
    """Summary of progress in a scenario"""
    scenario_id = serializers.IntegerField()
    scenario_name = serializers.CharField()
    scenario_slug = serializers.CharField()
    total_milestones = serializers.IntegerField()
    completed = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    not_started = serializers.IntegerField()
    percent = serializers.IntegerField()
    

class MilestoneSimpleSerializer(serializers.Serializer):
    """Simple milestone info for pending list"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    level = serializers.CharField()
    order = serializers.IntegerField()
    estimated_time = serializers.IntegerField()
    new_vocab_count = serializers.IntegerField()


class StartMilestoneSerializer(serializers.Serializer):
    """Input for starting a milestone"""
    milestone_id = serializers.IntegerField()


class CompleteMilestoneSerializer(serializers.Serializer):
    """Input for completing a milestone"""
    milestone_id = serializers.IntegerField()
    score = serializers.IntegerField(min_value=0, max_value=100, default=100)
    time_spent_seconds = serializers.IntegerField(min_value=0, default=0)


class UserExerciseAttemptSerializer(serializers.ModelSerializer):
    """Serializer for exercise attempts"""
    
    class Meta:
        model = UserExerciseAttempt
        fields = [
            'id',
            'exercise_type',
            'exercise_id',
            'is_correct',
            'score',
            'time_spent_seconds',
            'hints_used',
            'xp_earned',
            'completed_at',
        ]
        read_only_fields = ['id', 'xp_earned', 'completed_at']
