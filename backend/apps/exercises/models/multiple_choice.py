"""
Multiple Choice Exercise - Select the correct option
"""
from django.db import models
from .base import ExerciseBase


class MultipleChoiceExercise(ExerciseBase):
    """
    Exercise with multiple options, one or more correct.
    
    Example:
        Question: "What is the past tense of 'go'?"
        Options: ["goed", "went", "gone", "going"]
        Correct: "went"
    """
    
    # Pregunta o contexto
    question = models.TextField(
        help_text="Pregunta o contexto para el ejercicio"
    )
    
    # Opciones
    options = models.JSONField(
        help_text="Lista de opciones, ej: ['am', 'is', 'are', 'be']"
    )
    
    # Índice(s) de respuesta(s) correcta(s) - 0-based
    correct_indices = models.JSONField(
        help_text="Índices de opciones correctas, ej: [0] o [0, 2]"
    )
    
    # ¿Permite múltiples respuestas?
    allow_multiple = models.BooleanField(
        default=False,
        help_text="Si true, usuario puede seleccionar múltiples"
    )
    
    # Explicación de la respuesta
    explanation = models.TextField(
        blank=True,
        help_text="Explicación de por qué es correcta"
    )
    
    # Imagen opcional
    image_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = 'Multiple Choice Exercise'
        verbose_name_plural = 'Multiple Choice Exercises'
    
    def __str__(self):
        return f"[{self.level}] {self.question[:50]}"
    
    def save(self, *args, **kwargs):
        if not self.instructions:
            if self.allow_multiple:
                self.instructions = "Selecciona todas las opciones correctas"
            else:
                self.instructions = "Selecciona la opción correcta"
        super().save(*args, **kwargs)
    
    def get_correct_options(self):
        """Retorna las opciones correctas"""
        return [self.options[i] for i in self.correct_indices if i < len(self.options)]
    
    def check_answer(self, user_answer):
        """
        Valida la respuesta.
        user_answer: índice (int) o lista de índices
        """
        if isinstance(user_answer, int):
            user_indices = [user_answer]
        else:
            user_indices = list(user_answer)
        
        correct_set = set(self.correct_indices)
        user_set = set(user_indices)
        
        if user_set == correct_set:
            feedback = self.explanation if self.explanation else "¡Correcto! ✅"
            return True, feedback
        
        correct_display = ', '.join(self.get_correct_options())
        return False, f"Incorrecto. Respuesta(s) correcta(s): {correct_display}"
    
    def get_display_data(self):
        """Data para el frontend"""
        return {
            'id': self.id,
            'type': 'multiple_choice',
            'level': self.level,
            'instructions': self.instructions,
            'question': self.question,
            'options': self.options,
            'allow_multiple': self.allow_multiple,
            'image_url': self.image_url,
            'xp_reward': self.xp_reward,
            'difficulty': self.difficulty,
        }
