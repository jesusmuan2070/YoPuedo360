from django.contrib import admin
from .models import GrammarUnit, GrammarInMilestone, UserGrammarProgress


@admin.register(GrammarUnit)
class GrammarUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'grammatical_category', 'pedagogical_sequence', 'is_universal']
    list_filter = ['level', 'grammatical_category', 'is_universal']
    search_fields = ['name', 'slug', 'form']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['pedagogical_sequence', 'level']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('slug', 'name', 'level', 'grammatical_category')
        }),
        ('Forma y Significado', {
            'fields': ('form', 'meaning_en', 'meaning_es')
        }),
        ('Metadata Estructural', {
            'fields': ('structural_metadata', 'examples', 'common_error_patterns'),
            'classes': ('collapse',)
        }),
        ('Pedagógico', {
            'fields': ('pedagogical_sequence', 'is_universal')
        }),
        ('Sistema', {
            'fields': ('source', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GrammarInMilestone)
class GrammarInMilestoneAdmin(admin.ModelAdmin):
    list_display = ['grammar', 'milestone', 'introduction_order', 'importance_weight', 'is_primary_focus']
    list_filter = ['importance_weight', 'is_primary_focus', 'milestone__scenario']
    search_fields = ['grammar__name', 'milestone__name', 'context_example']
    autocomplete_fields = ['grammar', 'milestone']
    ordering = ['milestone', 'introduction_order']
    
    fieldsets = (
        ('Relación', {
            'fields': ('grammar', 'milestone')
        }),
        ('Contextualización', {
            'fields': ('context_example', 'suggested_vocabulary_words')
        }),
        ('Importancia', {
            'fields': ('importance_weight', 'is_primary_focus')
        }),
        ('Orden', {
            'fields': ('introduction_order',)
        }),
    )


@admin.register(UserGrammarProgress)
class UserGrammarProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'grammar', 'status', 'next_review', 'times_correct', 'times_incorrect']
    list_filter = ['status', 'grammar__level']
    search_fields = ['user__username', 'grammar__name']
    readonly_fields = ['created_at', 'updated_at', 'last_reviewed']
    date_hierarchy = 'next_review'
    
    fieldsets = (
        ('Usuario y Grammar', {
            'fields': ('user', 'grammar')
        }),
        ('SRS', {
            'fields': ('status', 'ease_factor', 'interval', 'repetitions', 'next_review')
        }),
        ('Estadísticas', {
            'fields': ('times_correct', 'times_incorrect', 'last_reviewed')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
