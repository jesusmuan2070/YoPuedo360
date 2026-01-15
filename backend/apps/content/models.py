"""
Content Models - Vocabulary and SRS (Spaced Repetition System)
Manages the 5k active + 15k passive vocabulary goal
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Vocabulary(models.Model):
    """
    Palabra individual del vocabulario.
    Objetivo: 5,000 activas + 15,000 pasivas = C2
    """
    LEVEL_CHOICES = [
        ('A1', 'A1'), ('A2', 'A2'),
        ('B1', 'B1'), ('B2', 'B2'),
        ('C1', 'C1'), ('C2', 'C2'),
    ]
    
    # La palabra
    word = models.CharField(max_length=100, db_index=True)
    lemma = models.CharField(max_length=100)  # forma base (run, runs, running → run)
    
    # Idiomas
    source_language = models.CharField(max_length=5, default='es')  # idioma del usuario
    target_language = models.CharField(max_length=5, default='en')  # idioma a aprender
    
    # Traducción principal
    translation = models.CharField(max_length=200)
    
    # Metadatos
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, db_index=True)
    frequency_rank = models.PositiveIntegerField(default=0)  # 1 = más común
    part_of_speech = models.CharField(max_length=20, blank=True)  # noun, verb, adj
    
    # Audio/Pronunciación
    pronunciation = models.CharField(max_length=100, blank=True)  # IPA
    audio_url = models.URLField(blank=True)
    
    # Ejemplo de uso
    example_sentence = models.TextField(blank=True)
    example_translation = models.TextField(blank=True)
    
    # Clasificación
    is_active_vocab = models.BooleanField(default=False)  # palabra activa vs pasiva goal
    
    class Meta:
        verbose_name_plural = 'Vocabulary'
        ordering = ['frequency_rank', 'word']
        indexes = [
            models.Index(fields=['level', 'target_language']),
            models.Index(fields=['frequency_rank']),
        ]
    
    def __str__(self):
        return f"{self.word} ({self.level})"


class VocabularyUsage(models.Model):
    """
    Relaciona vocabulario con escenarios.
    Permite que una palabra aparezca en múltiples escenarios con diferente relevancia.
    """
    from apps.memory_palace.models import Scenario
    
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='usages')
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='vocabulary_usages')
    
    # Qué tan relevante es esta palabra para el escenario (1-5)
    weight = models.PositiveIntegerField(default=3)
    
    # Contexto específico del escenario
    context_example = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['vocabulary', 'scenario']


class UserVocabularyProgress(models.Model):
    """
    Sistema SRS (Spaced Repetition System) por usuario.
    Trackea el progreso de cada palabra.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vocabulary_progress')
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
    
    # Estado de la palabra
    STATUS_CHOICES = [
        ('new', 'Nueva'),
        ('learning', 'Aprendiendo'),
        ('review', 'En repaso'),
        ('mastered', 'Dominada'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    # SRS Algorithm fields (similar a Anki)
    ease_factor = models.FloatField(default=2.5)  # Multiplicador de intervalo
    interval = models.PositiveIntegerField(default=1)  # Días hasta próximo repaso
    repetitions = models.PositiveIntegerField(default=0)  # Veces repasada correctamente
    
    # Cuándo repasar
    next_review = models.DateField(default=timezone.now)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    
    # Tipo de conocimiento
    is_active = models.BooleanField(default=False)  # ¿Palabra activa (puede usarla)?
    
    # Estadísticas
    times_correct = models.PositiveIntegerField(default=0)
    times_incorrect = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'vocabulary']
        indexes = [
            models.Index(fields=['user', 'next_review']),
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.vocabulary.word} ({self.status})"
    
    def process_review(self, quality):
        """
        Procesa el resultado de un repaso.
        quality: 0-5 (0=fail, 3=hard, 4=good, 5=easy)
        Basado en algoritmo SM-2 de Anki.
        """
        if quality < 3:
            # Respuesta incorrecta - reiniciar
            self.repetitions = 0
            self.interval = 1
            self.times_incorrect += 1
        else:
            # Respuesta correcta
            self.times_correct += 1
            
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)
            
            self.repetitions += 1
        
        # Ajustar ease factor
        self.ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        
        # Calcular próximo repaso
        self.next_review = timezone.now().date() + timedelta(days=self.interval)
        self.last_reviewed = timezone.now()
        
        # Actualizar status
        if self.repetitions >= 5 and self.ease_factor >= 2.0:
            self.status = 'mastered'
            self.is_active = True  # Palabra dominada = activa
        elif self.repetitions >= 2:
            self.status = 'review'
        elif self.repetitions >= 1:
            self.status = 'learning'
        else:
            self.status = 'new'
        
        self.save()
    
    @classmethod
    def get_words_for_review(cls, user, limit=20):
        """Obtiene palabras que necesitan repaso hoy"""
        today = timezone.now().date()
        return cls.objects.filter(
            user=user,
            next_review__lte=today
        ).select_related('vocabulary').order_by('next_review')[:limit]
    
    @classmethod
    def get_vocabulary_stats(cls, user):
        """Estadísticas de vocabulario del usuario"""
        from django.db.models import Count
        
        stats = cls.objects.filter(user=user).aggregate(
            total=Count('id'),
            new=Count('id', filter=models.Q(status='new')),
            learning=Count('id', filter=models.Q(status='learning')),
            review=Count('id', filter=models.Q(status='review')),
            mastered=Count('id', filter=models.Q(status='mastered')),
            active=Count('id', filter=models.Q(is_active=True)),
        )
        return stats


# ============================================
# GRAMÁTICA - Track de estructuras por nivel
# ============================================

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
        unique_together = ['user', 'topic']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'next_review']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.topic.name} ({self.status})"
    
    @classmethod
    def get_pending_topics(cls, user, level=None):
        """Gramática que el usuario no ha completado"""
        from apps.users.models import LearningProfile
        
        if level is None:
            try:
                profile = LearningProfile.objects.get(user=user)
                level = profile.cefr_level or 'A1'
            except LearningProfile.DoesNotExist:
                level = 'A1'
        
        completed = cls.objects.filter(
            user=user,
            status__in=['completed', 'mastered']
        ).values_list('topic_id', flat=True)
        
        return GrammarTopic.objects.filter(
            level=level,
            is_active=True
        ).exclude(id__in=completed).order_by('order')
    
    @classmethod
    def get_grammar_stats(cls, user):
        """Estadísticas de gramática del usuario"""
        from django.db.models import Count
        
        stats = cls.objects.filter(user=user).aggregate(
            total=Count('id'),
            not_started=Count('id', filter=models.Q(status='not_started')),
            in_progress=Count('id', filter=models.Q(status='in_progress')),
            completed=Count('id', filter=models.Q(status='completed')),
            mastered=Count('id', filter=models.Q(status='mastered')),
        )
        return stats


class MilestoneGrammar(models.Model):
    """
    Vincula gramática a milestones.
    Cada milestone puede enseñar/practicar cierta gramática.
    """
    from apps.memory_palace.models import Milestone
    
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name='grammar_focus')
    topic = models.ForeignKey(GrammarTopic, on_delete=models.CASCADE)
    
    is_primary = models.BooleanField(default=False)  # Foco principal del milestone
    
    class Meta:
        unique_together = ['milestone', 'topic']
    
    def __str__(self):
        return f"{self.milestone} → {self.topic.name}"

