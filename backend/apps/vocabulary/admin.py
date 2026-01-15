"""
Vocabulary Admin
"""
from django.contrib import admin
from .models import Vocabulary, VocabularyUsage, UserVocabularyProgress


@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ['word', 'translation', 'level', 'frequency_rank', 'part_of_speech']
    list_filter = ['level', 'target_language', 'part_of_speech']
    search_fields = ['word', 'translation']
    ordering = ['frequency_rank', 'word']


@admin.register(UserVocabularyProgress)
class UserVocabularyProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'vocabulary', 'status', 'next_review', 'repetitions']
    list_filter = ['status', 'is_active']
    search_fields = ['user__username', 'vocabulary__word']
    date_hierarchy = 'next_review'
