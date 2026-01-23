"""
Admin configuration for Users app.
Provides management interface for Users, LearningProfiles, and DailyActivity.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, LearningProfile, DailyActivity


class LearningProfileInline(admin.StackedInline):
    """Inline editor for LearningProfile within User admin."""
    model = LearningProfile
    can_delete = False
    verbose_name = 'Learning Profile'
    verbose_name_plural = 'Learning Profile'
    
    fieldsets = (
        ('Progress', {
            'fields': ('current_level', 'total_xp', 'cefr_level', 'streak_days', 'longest_streak')
        }),
        ('Goals & Preferences', {
            'fields': ('learning_goal', 'daily_goal_minutes', 'profession', 'work_domain')
        }),
        ('Languages', {
            'fields': ('native_language', 'target_language')
        }),
        ('Learning Style', {
            'fields': ('primary_style', 'visual_score', 'auditory_score', 'kinesthetic_score'),
            'classes': ('collapse',)
        }),
        ('Onboarding', {
            'fields': ('onboarding_completed', 'onboarding_step'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('current_level', 'total_xp', 'streak_days', 'longest_streak')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced User admin with learning profile integration."""
    
    list_display = (
        'username', 'email', 'get_cefr_level', 'get_total_xp', 
        'get_streak', 'is_active', 'last_activity'
    )
    list_filter = ('is_active', 'is_staff', 'date_joined', 'last_activity')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-last_activity',)
    
    inlines = [LearningProfileInline]
    
    # Add custom fields to the default fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('OAuth & Profile', {
            'fields': ('google_id', 'apple_id', 'avatar_url'),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(description='CEFR', ordering='learning_profile__cefr_level')
    def get_cefr_level(self, obj):
        profile = getattr(obj, 'learning_profile', None)
        if profile:
            colors = {
                'A1': '#4CAF50', 'A2': '#8BC34A',
                'B1': '#FFC107', 'B2': '#FF9800',
                'C1': '#F44336', 'C2': '#9C27B0'
            }
            color = colors.get(profile.cefr_level, '#666')
            return format_html(
                '<span style="background:{}; color:white; padding:2px 8px; border-radius:4px;">{}</span>',
                color, profile.cefr_level
            )
        return '-'
    
    @admin.display(description='XP', ordering='learning_profile__total_xp')
    def get_total_xp(self, obj):
        profile = getattr(obj, 'learning_profile', None)
        return f"{profile.total_xp:,}" if profile else '-'
    
    @admin.display(description='Streak', ordering='learning_profile__streak_days')
    def get_streak(self, obj):
        profile = getattr(obj, 'learning_profile', None)
        if profile and profile.streak_days > 0:
            fire = '🔥' if profile.streak_days >= 7 else ''
            return f"{profile.streak_days} {fire}"
        return '0'


@admin.register(LearningProfile)
class LearningProfileAdmin(admin.ModelAdmin):
    """Admin for LearningProfile with useful filters and actions."""
    
    list_display = (
        'user', 'cefr_level', 'current_level', 'total_xp_display', 
        'streak_display', 'daily_goal_minutes', 'learning_goal', 
        'onboarding_completed'
    )
    list_filter = (
        'cefr_level', 'learning_goal', 'onboarding_completed', 
        'primary_style', 'current_level'
    )
    search_fields = ('user__username', 'user__email', 'profession')
    ordering = ('-total_xp',)
    
    readonly_fields = ('created_at', 'updated_at', 'current_level')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Progress', {
            'fields': ('cefr_level', 'current_level', 'total_xp', 'streak_days', 'longest_streak')
        }),
        ('Goals', {
            'fields': ('learning_goal', 'daily_goal_minutes', 'goals', 'interests')
        }),
        ('Personalization', {
            'fields': ('profession', 'work_domain', 'hobbies')
        }),
        ('Languages', {
            'fields': ('native_language', 'target_language')
        }),
        ('Learning Style', {
            'fields': ('primary_style', 'visual_score', 'auditory_score', 'kinesthetic_score')
        }),
        ('Onboarding', {
            'fields': ('onboarding_completed', 'onboarding_step')
        }),
        ('AI & Memory Palace', {
            'fields': ('preferred_ai_provider', 'current_world_id', 'current_room_id'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(description='Total XP')
    def total_xp_display(self, obj):
        return f"{obj.total_xp:,}"
    
    @admin.display(description='Streak')
    def streak_display(self, obj):
        if obj.streak_days >= 30:
            return format_html('<span style="color:gold;">🔥 {} days</span>', obj.streak_days)
        elif obj.streak_days >= 7:
            return f"🔥 {obj.streak_days} days"
        elif obj.streak_days > 0:
            return f"{obj.streak_days} days"
        return "0"
    
    # Custom admin actions
    actions = ['reset_streak', 'award_bonus_xp']
    
    @admin.action(description='Reset streak to 0')
    def reset_streak(self, request, queryset):
        count = queryset.update(streak_days=0)
        self.message_user(request, f"Reset streak for {count} profiles.")
    
    @admin.action(description='Award 100 bonus XP')
    def award_bonus_xp(self, request, queryset):
        from django.db.models import F
        count = queryset.update(total_xp=F('total_xp') + 100)
        self.message_user(request, f"Awarded 100 XP to {count} profiles.")


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    """Admin for DailyActivity - mostly read-only for debugging."""
    
    list_display = (
        'user', 'date', 'minutes_studied', 'xp_earned', 
        'exercises_completed', 'daily_goal_met'
    )
    list_filter = ('date', 'daily_goal_met')
    search_fields = ('user__username', 'user__email')
    ordering = ('-date', '-id')
    date_hierarchy = 'date'
    
    readonly_fields = (
        'user', 'date', 'minutes_studied', 'xp_earned',
        'exercises_completed', 'lessons_completed', 
        'words_learned', 'words_reviewed', 'daily_goal_met'
    )
    
    def has_add_permission(self, request):
        # Activities should only be created by the system
        return False
    
    def has_change_permission(self, request, obj=None):
        # Allow viewing but not editing
        return False
