"""
Grammar Admin
"""
from django.contrib import admin
from .models import GrammarUnit, GrammarTopic, GrammarLesson, UserGrammarProgress


@admin.register(GrammarUnit)
class GrammarUnitAdmin(admin.ModelAdmin):
    list_display = ['slug', 'form', 'meaning', 'level']
    list_filter = ['level']
    search_fields = ['slug', 'form', 'meaning']
    ordering = ['level', 'slug']


@admin.register(GrammarTopic)
class GrammarTopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'order', 'estimated_time', 'is_active']
    list_filter = ['level', 'is_active']
    search_fields = ['name', 'name_es']
    ordering = ['level', 'order']


@admin.register(GrammarLesson)
class GrammarLessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic', 'order', 'estimated_time']
    list_filter = ['topic__level']
    search_fields = ['name', 'topic__name']
    ordering = ['topic', 'order']


@admin.register(UserGrammarProgress)
class UserGrammarProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'status', 'score', 'practice_count']
    list_filter = ['status']
    search_fields = ['user__username', 'topic__name']
    date_hierarchy = 'last_practiced'
