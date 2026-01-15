from django.contrib import admin
from .models import WordOrderExercise, FillBlankExercise, MultipleChoiceExercise, MatchingExercise, ExerciseAttempt


@admin.register(WordOrderExercise)
class WordOrderExerciseAdmin(admin.ModelAdmin):
    list_display = ['id', 'level', 'sentence', 'difficulty', 'is_active']
    list_filter = ['level', 'difficulty', 'is_active']
    search_fields = ['sentence', 'translation']


@admin.register(FillBlankExercise)
class FillBlankExerciseAdmin(admin.ModelAdmin):
    list_display = ['id', 'level', 'sentence_with_blanks', 'difficulty', 'is_active']
    list_filter = ['level', 'difficulty', 'is_active']
    search_fields = ['sentence_with_blanks']


@admin.register(MultipleChoiceExercise)
class MultipleChoiceExerciseAdmin(admin.ModelAdmin):
    list_display = ['id', 'level', 'question', 'difficulty', 'is_active']
    list_filter = ['level', 'difficulty', 'is_active']
    search_fields = ['question']


@admin.register(MatchingExercise)
class MatchingExerciseAdmin(admin.ModelAdmin):
    list_display = ['id', 'level', 'context', 'difficulty', 'is_active']
    list_filter = ['level', 'difficulty', 'is_active']
    search_fields = ['context']


@admin.register(ExerciseAttempt)
class ExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'exercise_type', 'exercise_id', 'is_correct', 'xp_earned', 'completed_at']
    list_filter = ['exercise_type', 'is_correct', 'completed_at']
    search_fields = ['user__username']
