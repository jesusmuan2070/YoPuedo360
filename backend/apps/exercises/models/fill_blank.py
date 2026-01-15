"""
Fill in the Blank Exercise - Complete sentences with missing words
"""
from django.db import models
from .base import ExerciseBase


class FillBlankExercise(ExerciseBase):
    """
    Exercise where user fills in missing word(s).
    
    Example:
        Display: "I ___ a teacher" 
        Options: ["am", "is", "are"]
        Answer: "am"
    """
    
    # Oración con blanks marcados como ___
    sentence_with_blanks = models.CharField(
        max_length=300,
        help_text="Oración con ___ donde va la respuesta"
    )
    
    # Respuesta(s) correcta(s)
    correct_answers = models.JSONField(
        default=list,
        help_text="Lista de respuestas correctas, ej: ['am', 'I am']"
    )
    
    # Opciones (si es multiple choice style)
    options = models.JSONField(
        default=list,
        blank=True,
        help_text="Opciones para elegir, ej: ['am', 'is', 'are']"
    )
    
    # Oración completa (para mostrar después)
    sentence_complete = models.CharField(
        max_length=300,
        blank=True,
        help_text="Oración completa para mostrar como feedback"
    )
    
    # Hint/pista
    hint = models.CharField(
        max_length=100,
        blank=True,
        help_text="Pista opcional, ej: '(verbo to be)'"
    )
    
    # Traducción
    translation = models.CharField(max_length=300, blank=True)
    
    class Meta:
        verbose_name = 'Fill in the Blank Exercise'
        verbose_name_plural = 'Fill in the Blank Exercises'
    
    def __str__(self):
        return f"[{self.level}] {self.sentence_with_blanks[:50]}"
    
    def save(self, *args, **kwargs):
        if not self.instructions:
            self.instructions = "Completa el espacio en blanco"
        super().save(*args, **kwargs)
    
    def check_answer(self, user_answer):
        """Valida la respuesta del usuario"""
        user_normalized = str(user_answer).lower().strip()
        
        for correct in self.correct_answers:
            if user_normalized == correct.lower().strip():
                return True, "¡Correcto! ✅"
        
        correct_display = self.correct_answers[0] if self.correct_answers else "?"
        return False, f"Incorrecto. La respuesta es: {correct_display}"
    
    def get_display_data(self):
        """Data para el frontend"""
        return {
            'id': self.id,
            'type': 'fill_blank',
            'level': self.level,
            'instructions': self.instructions,
            'sentence': self.sentence_with_blanks,
            'options': self.options,
            'hint': self.hint,
            'translation': self.translation,
            'xp_reward': self.xp_reward,
            'difficulty': self.difficulty,
        }
