"""
Matching Exercise - Connect items from two columns
"""
from django.db import models
from .base import ExerciseBase


class MatchingExercise(ExerciseBase):
    """
    Exercise where user matches items between two columns.
    
    Example:
        Left: ["Hello", "Goodbye", "Thank you"]
        Right: ["Adiós", "Hola", "Gracias"]
        Correct pairs: {0: 1, 1: 0, 2: 2}
    """
    
    # Columna izquierda (palabras/frases en inglés)
    left_items = models.JSONField(
        help_text="Items de la columna izquierda"
    )
    
    # Columna derecha (traducciones o matches)
    right_items = models.JSONField(
        help_text="Items de la columna derecha"
    )
    
    # Mapeo correcto: {índice_izq: índice_der}
    correct_pairs = models.JSONField(
        help_text="Mapeo de índices, ej: {'0': 1, '1': 0, '2': 2}"
    )
    
    # Contexto/tema
    context = models.CharField(
        max_length=100,
        blank=True,
        help_text="Tema del matching, ej: 'Saludos'"
    )
    
    class Meta:
        verbose_name = 'Matching Exercise'
        verbose_name_plural = 'Matching Exercises'
    
    def __str__(self):
        return f"[{self.level}] Matching: {self.context or 'Exercise'}"
    
    def save(self, *args, **kwargs):
        if not self.instructions:
            self.instructions = "Conecta cada elemento con su pareja correcta"
        super().save(*args, **kwargs)
    
    def check_answer(self, user_pairs):
        """
        Valida los pares del usuario.
        user_pairs: dict {índice_izq: índice_der}
        """
        # Normalizar keys a strings para comparación
        correct = {str(k): v for k, v in self.correct_pairs.items()}
        user = {str(k): v for k, v in user_pairs.items()}
        
        if correct == user:
            return True, "¡Todas las parejas correctas! ✅"
        
        # Contar aciertos
        correct_count = sum(1 for k, v in user.items() if correct.get(k) == v)
        total = len(correct)
        
        return False, f"Tienes {correct_count} de {total} correctas"
    
    def get_display_data(self):
        """Data para el frontend"""
        import random
        
        # Desordenar la columna derecha para el display
        right_shuffled = self.right_items.copy()
        random.shuffle(right_shuffled)
        
        return {
            'id': self.id,
            'type': 'matching',
            'level': self.level,
            'instructions': self.instructions,
            'left_items': self.left_items,
            'right_items': right_shuffled,  # Desordenados
            'context': self.context,
            'xp_reward': self.xp_reward,
            'difficulty': self.difficulty,
        }
