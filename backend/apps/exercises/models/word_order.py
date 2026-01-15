"""
Word Order Exercise - Arrange words to form correct sentences
"""
import random
from django.db import models
from .base import ExerciseBase


class WordOrderExercise(ExerciseBase):
    """
    Exercise where user arranges shuffled words into correct order.
    
    Example:
        Correct: "I am a teacher"
        Display: ["teacher", "am", "I", "a"] (shuffled)
        User drags to: ["I", "am", "a", "teacher"]
    """
    
    # La oración correcta
    sentence = models.CharField(
        max_length=300,
        help_text="Oración correcta, ej: 'I am a teacher'"
    )
    
    # Palabras desordenadas (se puede generar automáticamente)
    words_shuffled = models.JSONField(
        default=list,
        help_text="Lista de palabras desordenadas"
    )
    
    # Traducción para ayuda
    translation = models.CharField(
        max_length=300,
        blank=True,
        help_text="Traducción al español"
    )
    
    # Audio de la oración (opcional)
    audio_url = models.URLField(blank=True)
    
    # Alternativas aceptables (si hay múltiples respuestas correctas)
    alternative_answers = models.JSONField(
        default=list,
        help_text="Otras respuestas válidas, ej: ['I'm a teacher']"
    )
    
    class Meta:
        verbose_name = 'Word Order Exercise'
        verbose_name_plural = 'Word Order Exercises'
    
    def __str__(self):
        return f"[{self.level}] {self.sentence[:50]}"
    
    def save(self, *args, **kwargs):
        # Auto-generar palabras desordenadas si no existen
        if not self.words_shuffled and self.sentence:
            self.words_shuffled = self.shuffle_words()
        
        # Auto-generar instrucciones si no existen
        if not self.instructions:
            self.instructions = "Ordena las palabras para formar la oración correcta"
        
        super().save(*args, **kwargs)
    
    def shuffle_words(self):
        """Genera lista de palabras desordenadas"""
        words = self.sentence.split()
        shuffled = words.copy()
        
        # Asegurar que esté realmente desordenado
        attempts = 0
        while shuffled == words and attempts < 10:
            random.shuffle(shuffled)
            attempts += 1
        
        return shuffled
    
    def get_words(self):
        """Retorna palabras desordenadas (regenera si es necesario)"""
        if self.words_shuffled:
            return self.words_shuffled
        return self.shuffle_words()
    
    def check_answer(self, user_answer):
        """
        Valida la respuesta del usuario.
        
        Args:
            user_answer: list of words in user's order, or string
        
        Returns:
            (is_correct: bool, feedback: str)
        """
        # Normalizar respuesta
        if isinstance(user_answer, list):
            user_sentence = ' '.join(user_answer)
        else:
            user_sentence = str(user_answer)
        
        # Normalizar para comparación (lowercase, strip)
        user_normalized = user_sentence.lower().strip()
        correct_normalized = self.sentence.lower().strip()
        
        # Verificar respuesta principal
        if user_normalized == correct_normalized:
            return True, "¡Perfecto! ✅"
        
        # Verificar alternativas
        for alt in self.alternative_answers:
            if user_normalized == alt.lower().strip():
                return True, "¡Correcto! ✅"
        
        # Incorrecto - dar feedback útil
        return False, f"Incorrecto. La respuesta correcta es: {self.sentence}"
    
    def get_display_data(self):
        """Data para el frontend"""
        return {
            'id': self.id,
            'type': 'word_order',
            'level': self.level,
            'instructions': self.instructions,
            'words': self.get_words(),
            'translation': self.translation,
            'audio_url': self.audio_url,
            'xp_reward': self.xp_reward,
            'difficulty': self.difficulty,
        }
    
    @classmethod
    def create_from_sentence(cls, sentence, translation='', level='A1', **kwargs):
        """
        Factory method to create exercise from a sentence.
        
        Usage:
            exercise = WordOrderExercise.create_from_sentence(
                "I am a student",
                translation="Soy estudiante",
                level="A1"
            )
        """
        return cls.objects.create(
            sentence=sentence,
            translation=translation,
            level=level,
            **kwargs
        )
