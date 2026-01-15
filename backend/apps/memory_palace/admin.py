"""
Memory Palace Admin - Manage scenarios, tags, and milestones
"""

from django.contrib import admin
from .models import Tag, Scenario, Milestone, UserScenarioProgress


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['type', 'value', 'display_name', 'icon']
    list_filter = ['type']
    search_fields = ['value', 'display_name']
    ordering = ['type', 'value']


class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 1
    ordering = ['level', 'order']


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'slug', 'difficulty_min', 'difficulty_max', 'is_active']
    list_filter = ['is_active', 'difficulty_min', 'tags']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['tags']
    inlines = [MilestoneInline]
    ordering = ['order', 'name']


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['scenario', 'level', 'order', 'name', 'estimated_time']
    list_filter = ['level', 'scenario']
    search_fields = ['name', 'description']
    ordering = ['scenario', 'level', 'order']


@admin.register(UserScenarioProgress)
class UserScenarioProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'scenario', 'is_started', 'is_completed', 'stars_earned', 'last_activity']
    list_filter = ['is_completed', 'is_started', 'scenario']
    search_fields = ['user__username', 'scenario__name']
    raw_id_fields = ['user', 'scenario', 'current_milestone']
