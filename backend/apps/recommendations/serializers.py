"""
Recommendation Serializers
"""

from rest_framework import serializers
from apps.memory_palace.models import Scenario


class RecommendedScenarioSerializer(serializers.ModelSerializer):
    """Serializer for recommended scenarios."""
    
    tags = serializers.SerializerMethodField()
    milestones_count = serializers.SerializerMethodField()
    difficulty_min = serializers.CharField(source='min_level', read_only=True)
    difficulty_max = serializers.SerializerMethodField()
    
    class Meta:
        model = Scenario
        fields = [
            'id', 'slug', 'name', 'icon', 'description',
            'tags', 'difficulty_min', 'difficulty_max', 
            'milestones_count', 'is_active'
        ]
    
    def get_tags(self, obj):
        return [
            {'type': tag.type, 'value': tag.value, 'icon': tag.icon}
            for tag in obj.tags.all()
        ]
    
    def get_milestones_count(self, obj):
        return obj.milestones.count()
    
    def get_difficulty_max(self, obj):
        # Get max level from milestones if available
        levels = list(obj.milestones.values_list('level', flat=True).distinct())
        level_order = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        if levels:
            max_idx = max(level_order.index(l) for l in levels if l in level_order)
            return level_order[max_idx]
        return obj.min_level


class RecommendationResultSerializer(serializers.Serializer):
    """Serializer for recommendation results."""
    
    scenarios = RecommendedScenarioSerializer(many=True)
    total_count = serializers.IntegerField()
    user_level = serializers.CharField()
    applied_filters = serializers.ListField(child=serializers.CharField())

