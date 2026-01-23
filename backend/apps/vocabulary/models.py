"""
Vocabulary Models - SRS (Spaced Repetition System)
Manages the 5k active + 15k passive vocabulary goal
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from apps.users.services.xp_service import XPService

User = get_user_model()


class Vocabulary(models.Model):
    """
    Palabra universal - Vive 1 vez en el sistema.
    Datos pueden venir de: Oxford 3000, Cambridge Profile, o generación manual.
    
    Objetivo pedagógico: 5,000 activas + 15,000 pasivas = C2
    """
    LEVEL_CHOICES = [
        ('A1', 'A1'), ('A2', 'A2'),
        ('B1', 'B1'), ('B2', 'B2'),
        ('C1', 'C1'), ('C2', 'C2'),
    ]
    
    # ==========================================
    # IDENTIFICADORES
    # ==========================================
    word = models.CharField(
        max_length=100, 
        unique=True,  # Cada palabra solo existe 1 vez
        help_text='Palabra exacta (ej: swimming, swam, swims)'
    )
    lemma = models.CharField(
        max_length=100, 
        db_index=True,
        help_text='Forma base/diccionario (ej: swim)'
    )
    
    # ==========================================
    # CLASIFICACIÓN CEFR
    # ==========================================
    level = models.CharField(
        max_length=2, 
        choices=LEVEL_CHOICES, 
        db_index=True,
        help_text='Nivel CEFR de dificultad'
    )
    frequency_rank = models.PositiveIntegerField(
        default=0,
        help_text='Ranking de frecuencia (1=más común, 10000=raro). De Oxford/Cambridge.'
    )
    
    # ==========================================
    # LINGÜÍSTICO (Auto-detectado con spaCy)
    # ==========================================
    part_of_speech = models.CharField(
        max_length=20, 
        blank=True,
        help_text='Tipo gramatical: verb, noun, adjective, adverb, etc.'
    )
    
    # ==========================================
    # FORMAS MORFOLÓGICAS (Auto-generadas con Pattern.en)
    # ==========================================
    morphological_forms = models.JSONField(
        default=dict,
        blank=True,
        help_text='''Formas automáticas de la palabra. Ejemplos:
        Verbo: {"present": "swim", "past": "swam", "past_participle": "swum", "gerund": "swimming", "third_person": "swims"}
        Noun: {"singular": "child", "plural": "children"}
        Adj: {"positive": "happy", "comparative": "happier", "superlative": "happiest"}'''
    )
    
    # ==========================================
    # DEFINICIONES / TRADUCCIONES
    # ==========================================
    definition_en = models.TextField(
        blank=True,
        help_text='Definición en inglés simple (nivel apropiado)'
    )
    definition_es = models.TextField(
        blank=True,
        help_text='Definición/traducción en español'
    )
    
    # Legacy field (mantener compatibilidad)
    translation = models.CharField(
        max_length=200,
        blank=True,
        help_text='LEGACY: Usar definition_es en su lugar'
    )
    
    # ==========================================
    # PRONUNCIACIÓN
    # ==========================================
    phonetic = models.CharField(
        max_length=100, 
        blank=True,
        help_text='Notación fonética IPA (ej: /swɪm/)'
    )
    audio_url = models.URLField(
        blank=True,
        help_text='URL del archivo de audio MP3'
    )
    
    # Legacy field (mantener compatibilidad)
    pronunciation = models.CharField(
        max_length=100, 
        blank=True,
        help_text='LEGACY: Usar phonetic en su lugar'
    )
    
    # ==========================================
    # EJEMPLOS DE USO
    # ==========================================
    example_sentence = models.TextField(
        blank=True,
        help_text='Oración de ejemplo en inglés'
    )
    example_translation = models.TextField(
        blank=True,
        help_text='Traducción de la oración de ejemplo'
    )
    
    # ==========================================
    # METADATA DEL SISTEMA
    # ==========================================
    source = models.CharField(
        max_length=50,
        default='manual',
        choices=[
            ('oxford', 'Oxford 3000/5000'),
            ('cambridge', 'Cambridge Vocabulary Profile'),
            ('manual', 'Agregado manualmente'),
            ('pattern', 'Generado con Pattern.en'),
        ],
        help_text='Origen de los datos de esta palabra'
    )
    
    # Idiomas (mantener para multi-language futuro)
    source_language = models.CharField(max_length=5, default='es')
    target_language = models.CharField(max_length=5, default='en')
    
    # Clasificación pedagógica
    is_active_vocab = models.BooleanField(
        default=False,
        help_text='¿Palabra objetivo activo (producción) vs pasivo (comprensión)?'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'content_vocabulary'  # Backward compatibility
        verbose_name_plural = 'Vocabulary'
        ordering = ['frequency_rank', 'word']
        indexes = [
            models.Index(fields=['lemma', 'level']),
            models.Index(fields=['part_of_speech', 'level']),
            models.Index(fields=['level', 'target_language']),
            models.Index(fields=['frequency_rank']),
        ]
    
    def __str__(self):
        return f"{self.word} ({self.level})"
    
    def get_form(self, form_name):
        """
        Obtiene una forma morfológica específica.
        
        Args:
            form_name: 'past', 'gerund', 'plural', 'comparative', etc.
        
        Returns:
            str: La forma solicitada, o la palabra original si no existe
        """
        return self.morphological_forms.get(form_name, self.word)


class VocabularyUsage(models.Model):
    """
    ⚠️ LEGACY - DEPRECADO
    
    Este modelo conecta a Scenario (demasiado alto nivel).
    Usar VocabularyInMilestone que conecta a Milestone (más granular).
    
    Se mantiene por backward compatibility, pero NO usar en código nuevo.
    """
    from apps.scenarios.models import Scenario
    
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='usages')
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='vocabulary_usages')
    
    # Qué tan relevante es esta palabra para el escenario (1-5)
    weight = models.PositiveIntegerField(default=3)
    
    # Contexto específico del escenario
    context_example = models.TextField(blank=True)
    
    class Meta:
        db_table = 'content_vocabularyusage'  # Mantener nombre viejo
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
        db_table = 'content_uservocabularyprogress'  # Mantener nombre viejo
        unique_together = ['user', 'vocabulary']
        indexes = [
            models.Index(fields=['user', 'next_review']),
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.vocabulary.word} ({self.status})"
    
    def process_review(self, quality):
        """
        Procesa el resultado de un repaso y otorga XP.
        quality: 0-5 (0=fail, 3=hard, 4=good, 5=easy)
        Basado en algoritmo SM-2 de Anki.
        """
        old_status = self.status
        
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
        
        # Award XP via XPService
        cefr_level = getattr(self.vocabulary, 'level', 'A1') or 'A1'
        
        if quality >= 3:  # Correct review
            XPService.award_word_reviewed_xp(self.user, cefr_level)
        
        # Bonus XP for reaching 'mastered' status
        if self.status == 'mastered' and old_status != 'mastered':
            XPService.award_word_learned_xp(self.user, cefr_level)
    
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


class VocabularyInMilestone(models.Model):
    """
    CAPA 2: Conecta Vocabulary universal con Milestone específico.
    
    Permite reutilizar palabras en múltiples milestones con diferente contexto.
    Ejemplo: "please" en Restaurant vs "please" en Airport.
    """
    
    # Choices estáticas (mejor performance)
    IMPORTANCE_CHOICES = [
        (1, 'Opcional'),
        (2, 'Útil'),
        (3, 'Importante'),
        (4, 'Muy importante'),
        (5, 'Crítico'),
    ]
    
    vocabulary = models.ForeignKey(
        Vocabulary,
        on_delete=models.CASCADE,
        related_name='milestone_usages',
        help_text='Palabra del diccionario universal'
    )
    milestone = models.ForeignKey(
        'scenarios.Milestone',
        on_delete=models.CASCADE,
        related_name='vocabulary_items',
        help_text='Milestone donde se usa esta palabra'
    )
    
    # Contextualización específica del milestone
    context_usage = models.TextField(
        blank=True,
        help_text='Cómo se usa en este milestone específico. Ej: "Can I have a coffee?"'
    )
    
    # Importancia para este milestone (1-5)
    importance_weight = models.IntegerField(
        default=3,
        choices=IMPORTANCE_CHOICES,
        help_text='Importancia de esta palabra en este milestone'
    )
    
    # ¿Usuario debe producir o solo reconocer?
    is_active_target = models.BooleanField(
        default=False,
        help_text='True=Usuario debe poder DECIR esta palabra. False=Solo reconocerla.'
    )
    
    # Orden de introducción en el milestone
    introduction_order = models.PositiveIntegerField(
        default=1,
        help_text='Orden en que se introduce en este milestone (1=primero, 2=segundo, etc.)'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'vocabulary_in_milestone'
        unique_together = ['vocabulary', 'milestone']
        ordering = ['introduction_order']
        indexes = [
            models.Index(fields=['milestone', 'importance_weight']),
            models.Index(fields=['milestone', 'introduction_order']),
        ]
        verbose_name = 'Vocabulary in Milestone'
        verbose_name_plural = 'Vocabulary in Milestones'
    
    def __str__(self):
        return f"{self.vocabulary.word} in {self.milestone.name} (order: {self.introduction_order})"
