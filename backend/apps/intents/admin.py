from django.contrib import admin
from .models import (
    CommunicativeIntent,
    IntentGrammarDependency,
    IntentRealization,
    UserIntentProgress
)


@admin.register(CommunicativeIntent)
class CommunicativeIntentAdmin(admin.ModelAdmin):
    list_display = ['cefr_rank', 'name', 'level', 'category', 'is_core']
    list_filter = ['level', 'category', 'is_core', 'cefr_rank']
    search_fields = ['name', 'slug', 'description']
    ordering = ['level', 'cefr_rank', 'slug']
    
    fieldsets = (
        ('Identity', {
            'fields': ('slug', 'name', 'description', 'category')
        }),
        ('CEFR Level', {
            'fields': ('level', 'cefr_rank', 'is_core')
        }),
    )


@admin.register(IntentGrammarDependency)
class IntentGrammarDependencyAdmin(admin.ModelAdmin):
    list_display = ['intent', 'grammar', 'is_critical', 'order']
    list_filter = ['is_critical', 'intent__level']
    search_fields = ['intent__name', 'grammar__name']
    ordering = ['intent__cefr_rank', 'order']


@admin.register(IntentRealization)
class IntentRealizationAdmin(admin.ModelAdmin):
    list_display = ['intent', 'milestone', 'priority', 'is_primary', 'difficulty']
    list_filter = ['is_primary', 'milestone__level', 'difficulty']
    search_fields = ['intent__name', 'milestone__name']
    ordering = ['milestone', 'priority']
    
    fieldsets = (
        ('Connection', {
            'fields': ('intent', 'milestone')
        }),
        ('Examples', {
            'fields': ('example_chunks', 'example_chunks_es')
        }),
        ('Metadata', {
            'fields': ('difficulty', 'estimated_time', 'priority', 'is_primary')
        }),
    )


@admin.register(UserIntentProgress)
class UserIntentProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'intent', 'status', 'last_score', 'times_practiced']
    list_filter = ['status', 'intent__level']
    search_fields = ['user__username', 'intent__name']
    ordering = ['user', 'intent__cefr_rank']
