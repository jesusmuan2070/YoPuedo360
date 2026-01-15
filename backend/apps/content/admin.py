"""
Content Admin - Vocabulary management
"""

from django.contrib import admin
from .models import Vocabulary, VocabularyUsage, UserVocabularyProgress


@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ['word', 'translation', 'level', 'frequency_rank', 'part_of_speech', 'is_active_vocab']
    list_filter = ['level', 'target_language', 'part_of_speech', 'is_active_vocab']
    search_fields = ['word', 'translation', 'lemma']
    ordering = ['frequency_rank', 'word']


@admin.register(VocabularyUsage)
class VocabularyUsageAdmin(admin.ModelAdmin):
    list_display = ['vocabulary', 'scenario', 'weight']
    list_filter = ['scenario', 'weight']
    search_fields = ['vocabulary__word', 'scenario__name']
    raw_id_fields = ['vocabulary', 'scenario']


@admin.register(UserVocabularyProgress)
class UserVocabularyProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'vocabulary', 'status', 'is_active', 'next_review', 'repetitions']
    list_filter = ['status', 'is_active']
    search_fields = ['user__username', 'vocabulary__word']
    raw_id_fields = ['user', 'vocabulary']
    date_hierarchy = 'next_review'
