from rest_framework import serializers
from .models import User, LearningProfile

class LearningProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for LearningProfile.
    """
    class Meta:
        model = LearningProfile
        fields = [
            'native_language', 'target_language', 'learning_goal',
            'daily_goal_minutes', 'current_level', 'total_xp',
            'streak_days',
            # New fields
            'cefr_level', 'profession', 'interests', 'hobbies'
        ]
        read_only_fields = ['current_level', 'total_xp', 'streak_days']

class UserSerializer(serializers.ModelSerializer):
    """
    Main User serializer that includes the profile.
    Supports nested updates.
    """
    learning_profile = LearningProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'avatar_url', 'learning_profile']
        read_only_fields = ['username', 'email']

    def update(self, instance, validated_data):
        """
        Support writable nested 'learning_profile'.
        """
        profile_data = validated_data.pop('learning_profile', None)
        
        # Update User fields
        instance = super().update(instance, validated_data)
        
        # Update Profile fields if provided
        if profile_data:
            profile = instance.learning_profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
            
        return instance


class RecordSessionSerializer(serializers.Serializer):
    """
    Serializer for recording study sessions.
    Used by RecordSessionView to validate incoming data.
    """
    minutes = serializers.IntegerField(min_value=1, max_value=180)
    xp_earned = serializers.IntegerField(min_value=0, default=0, required=False)
    activity_type = serializers.ChoiceField(
        choices=['exercise', 'lesson', 'vocabulary', 'grammar', 'conversation'],
        required=False,
        default='lesson'
    )
