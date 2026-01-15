"""
Grammar Models - 4-Layer Architecture
Manages grammar rules, topics, and user progress
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class GrammarUnit(models.Model):
    """
    Unidad gramatical universal (Capa 1 - vive 1 vez).
    Ejemplo: can/can't para habilidad/permiso
    
    Esta es la regla gramatical base que existe independientemente
    de cualquier contexto o escenario.
    """
    # Identificador único
    slug = models.SlugField(unique=True, db_index=True)  # "can_cant_ability"
    
    # CEFR Level
    LEVEL_CHOICES = [
        ('A1', 'A1'), ('A2', 'A2'),
        ('B1', 'B1'), ('B2', 'B2'),
        ('C1', 'C1'), ('C2', 'C2'),
    ]
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, db_index=True)
    
    # Forma gramatical
    form = models.CharField(max_length=200)  # "can / can't"
    form_pattern = models.CharField(max_length=200, blank=True)  # "subject + can + verb"
    
    # Significado/función
    meaning = models.CharField(max_length=200)  # "ability / permission"
    meaning_es = models.CharField(max_length=200, blank=True)  # "habilidad / permiso"
    
    # Ejemplos universales (no ligados a contexto)
    examples = models.JSONField(default=list)
    # [
    #   {"en": "I can swim", "es": "Puedo nadar"},
    #   {"en": "She can't drive", "es": "Ella no puede manejar"}
    # ]
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['level', 'slug']
        verbose_name = "Grammar Unit"
        verbose_name_plural = "Grammar Units"
    
    def __str__(self):
        return f"[{self.level}] {self.form} - {self.meaning}"


class GrammarTopic(models.Model):
    """
    Tema gramatical (ej: Present Simple, Past Simple).
    Obligatorio para cada nivel CEFR.
    """
    LEVEL_CHOICES = [
        ('A1', 'A1'), ('A2', 'A2'),
        ('B1', 'B1'), ('B2', 'B2'),
        ('C1', 'C1'), ('C2', 'C2'),
    ]
    
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)  # "Present Simple"
    name_es = models.CharField(max_length=100, blank=True)  # "Presente Simple"
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, db_index=True)
    order = models.PositiveIntegerField()  # Orden obligatorio en el nivel
    
    description = models.TextField(blank=True)
    pattern = models.CharField(max_length=200, blank=True)  # "Subject + verb"
    examples = models.JSONField(default=list)  # ["I work", "She eats"]
    
    # Reglas y excepciones
    rules = models.JSONField(default=list)  # Reglas principales
    exceptions = models.JSONField(default=list)  # Excepciones comunes
    
    # Cuánto tiempo toma aprender
    estimated_time = models.PositiveIntegerField(default=30)  # minutos
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'content_grammartopic'  # Mantener nombre viejo
        ordering = ['level', 'order']
        unique_together = ['level', 'order']
    
    def __str__(self):
        return f"[{self.level}] {self.name}"


class GrammarLesson(models.Model):
    """
    Lección específica dentro de un tema gramatical.
    Ej: Present Simple → 1. Affirmative, 2. Negative, 3. Questions
    """
    topic = models.ForeignKey(GrammarTopic, on_delete=models.CASCADE, related_name='lessons')
    order = models.PositiveIntegerField()
    name = models.CharField(max_length=100)  # "Affirmative sentences"
    
    explanation = models.TextField()  # Explicación detallada
    examples = models.JSONField(default=list)  # Ejemplos con traducción
    
    # Ejercicios integrados
    exercises = models.JSONField(default=list)  # Ejercicios de práctica
    
    estimated_time = models.PositiveIntegerField(default=10)  # minutos
    
    class Meta:
        db_table = 'content_grammarlesson'  # Mantener nombre viejo
        ordering = ['topic', 'order']
        unique_together = ['topic', 'order']
    
    def __str__(self):
        return f"{self.topic.name} - {self.name}"


class UserGrammarProgress(models.Model):
    """
    Tracking de gramática aprendida por usuario.
    Permite saber qué temas ha completado y cuáles le faltan.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grammar_progress')
    topic = models.ForeignKey(GrammarTopic, on_delete=models.CASCADE)
    
    STATUS_CHOICES = [
        ('not_started', 'No iniciado'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completado'),
        ('mastered', 'Dominado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    # Fechas de tracking
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_practiced = models.DateTimeField(null=True, blank=True)
    
    # Puntuación y repasos
    score = models.PositiveIntegerField(default=0)  # 0-100
    practice_count = models.PositiveIntegerField(default=0)  # Veces practicado
    
    # SRS para gramática
    next_review = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'content_usergrammarprogress'  # Mantener nombre viejo
        unique_together = ['user', 'topic']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'next_review']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.topic.name} ({self.status})"
