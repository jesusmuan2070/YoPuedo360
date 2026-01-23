"""
Grammar Models - 4-Layer Architecture
Manages universal grammar patterns and their contextual usage in milestones
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from apps.users.services.xp_service import XPService

User = get_user_model()


class GrammarUnit(models.Model):
    """
    CAPA 1: Unidad gramatical UNIVERSAL
    
    Vive 1 vez en el sistema, se usa en MÚLTIPLES milestones.
    Ejemplos: "can + infinitive", "a/an articles", "present simple"
    
    Diferencia vs Vocabulary:
    - Vocabulary: Específico del dominio (coffee → restaurant)
    - Grammar: Universal (can → restaurant, airport, hotel)
    """
    
    LEVEL_CHOICES = [
        ('A1', 'A1'), ('A2', 'A2'),
        ('B1', 'B1'), ('B2', 'B2'),
        ('C1', 'C1'), ('C2', 'C2'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('de', 'German / Deutsch'),
        ('fr', 'French / Français'),
    ]
    
    CATEGORY_CHOICES = [
        # Universal categories (all languages)
        ('modal_verb', 'Modal Verbs'),
        ('article', 'Articles'),
        ('tense', 'Tenses'),
        ('pronoun', 'Pronouns'),
        ('preposition', 'Prepositions'),
        ('conjunction', 'Conjunctions'),
        ('question_form', 'Question Formation'),
        ('negation', 'Negation'),
        ('auxiliary', 'Auxiliary Verbs'),
        ('possessive', 'Possessives'),
        ('comparative', 'Comparatives/Superlatives'),
        ('gerund_infinitive', 'Gerunds & Infinitives'),
        ('adverb', 'Adverbs'),
        ('adjective', 'Adjectives'),
        ('verb', 'Verbs'),
        
        # Language-specific categories (primarily for DE, FR)
        ('gender', 'Grammatical Gender'),              # FR: M/F, DE: M/F/N
        ('case_system', 'Case System'),                # DE: Nominative, Accusative, Dative, Genitive
        ('declension', 'Declension'),                  # DE: Article/Adjective declension
        ('verb_mood', 'Verb Moods'),                   # FR: Subjunctive, Conditional, etc.
        ('adjective_agreement', 'Adjective Agreement'),# FR: Gender/number agreement
        ('word_order', 'Word Order'),                  # DE: V2, SOV in subordinates
    ]
    
    # ==========================================
    # IDENTIFICADORES
    # ==========================================
    slug = models.SlugField(
        db_index=True,
        help_text='Identificador único (ej: can-infinitive, a-an-articles, verbe-etre, artikel-der-die-das)'
    )
    
    target_language = models.CharField(
        max_length=5,
        default='en',
        choices=LANGUAGE_CHOICES,
        db_index=True,
        help_text='Idioma objetivo que este grammar unit enseña (ISO 639-1 code)'
    )
    
    name = models.CharField(
        max_length=100,
        help_text='Nombre descriptivo (ej: Can + Infinitive)'
    )
    
    # ==========================================
    # CLASIFICACIÓN
    # ==========================================
    level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        db_index=True,
        help_text='Nivel CEFR donde se introduce'
    )
    
    grammatical_category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        help_text='Categoría gramatical'
    )
    
    # ==========================================
    # FORMA Y SIGNIFICADO
    # ==========================================
    form = models.TextField(
        help_text='Forma gramatical (ej: can + base verb)'
    )
    
    meaning_en = models.TextField(
        help_text='Significado/función en inglés (ej: Ability, permission, possibility)'
    )
    
    meaning_es = models.TextField(
        help_text='Significado/función en español (ej: Habilidad, permiso, posibilidad)'
    )
    
    # ==========================================
    # METADATA ESTRUCTURAL (JSON)
    # ==========================================
    structural_metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text='''Metadata estructural de la gramática:
        {
          "pattern": "SUBJECT + can + BASE_VERB",
          "valid_forms": ["I can", "you can", "he can"],
          "conjugation": {"I": "can", "you": "can", "he/she/it": "can"},
          "components": {
            "modal": "can",
            "verb_form": "base/infinitive"
          }
        }'''
    )
    
    # ==========================================
    # EJEMPLOS UNIVERSALES
    # ==========================================
    examples = models.JSONField(
        default=list,
        blank=True,
        help_text='Ejemplos genéricos (no contextuales): [{"en": "I can swim", "es": "Puedo nadar"}]'
    )
    
    # ==========================================
    # ERRORES COMUNES
    # ==========================================
    common_error_patterns = models.JSONField(
        default=list,
        blank=True,
        help_text='''Errores comunes y correcciones:
        [
          {
            "error": "He cans swim",
            "rule": "Modal verbs don't add -s in 3rd person",
            "correction": "He can swim"
          }
        ]'''
    )
    
    # ==========================================
    # PEDAGÓGICO
    # ==========================================
    is_universal = models.BooleanField(
        default=True,
        help_text='¿Se usa en todos los contextos? (Siempre True para grammar)'
    )
    
    pedagogical_sequence = models.PositiveIntegerField(
        default=1,
        help_text='Orden GLOBAL de introducción (1=can, 2=will, 3=could, etc.)'
    )
    
    # ==========================================
    # METADATA
    # ==========================================
    source = models.CharField(
        max_length=50,
        default='manual',
        choices=[
            ('manual', 'Manual'),
            ('claude', 'Generated by Claude'),
            ('imported', 'Imported from dataset'),
        ],
        help_text='Origen de los datos'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'grammar_unit'
        ordering = ['target_language', 'pedagogical_sequence', 'level']
        verbose_name = 'Grammar Unit'
        verbose_name_plural = 'Grammar Units'
        unique_together = [['slug', 'target_language']]  # Permite mismo slug en diferentes idiomas
        indexes = [
            models.Index(fields=['level', 'grammatical_category']),
            models.Index(fields=['pedagogical_sequence']),
            models.Index(fields=['target_language', 'level']),
            models.Index(fields=['target_language', 'grammatical_category']),
        ]
    
    def __str__(self):
        return f"[{self.target_language.upper()}] [{self.level}] {self.name}"


class GrammarInMilestone(models.Model):
    """
    CAPA 2: Conecta GrammarUnit universal con Milestone específico
    
    Mismo grammar (can), diferente contexto:
    - Restaurant: "Can I have a coffee?"
    - Airport: "Can I see your passport?"
    - Hotel: "Can I check in?"
    """
    
    IMPORTANCE_CHOICES = [
        (1, 'Opcional'),
        (2, 'Útil'),
        (3, 'Importante'),
        (4, 'Muy importante'),
        (5, 'Crítico'),
    ]
    
    grammar = models.ForeignKey(
        GrammarUnit,
        on_delete=models.CASCADE,
        related_name='milestone_usages',
        help_text='Grammar unit universal'
    )
    
    milestone = models.ForeignKey(
        'scenarios.Milestone',
        on_delete=models.CASCADE,
        related_name='grammar_items',
        help_text='Milestone donde se usa este grammar'
    )
    
    # ==========================================
    # CONTEXTUALIZACIÓN
    # ==========================================
    context_example = models.JSONField(
        default=list,
        blank=True,
        help_text='Ejemplos: ["Example 1", "Example 2"]'
    )
    
    # ==========================================
    # IMPORTANCIA
    # ==========================================
    importance_weight = models.IntegerField(
        default=3,
        choices=IMPORTANCE_CHOICES,
        help_text='Importancia de este grammar en este milestone'
    )
    
    is_primary_focus = models.BooleanField(
        default=False,
        help_text='¿Este grammar es el OBJETIVO principal del milestone?'
    )
    
    # ==========================================
    # ORDEN PEDAGÓGICO
    # ==========================================
    introduction_order = models.PositiveIntegerField(
        default=1,
        help_text='Orden de introducción EN ESTE MILESTONE (grammar antes que vocabulario)'
    )
    
    # ==========================================
    # VOCABULARIO SUGERIDO
    # ==========================================
    suggested_vocabulary_words = models.JSONField(
        default=list,
        blank=True,
        help_text='Palabras que se combinan bien con este grammar en este contexto: ["coffee", "water", "menu"]'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'grammar_in_milestone'
        unique_together = ['grammar', 'milestone']
        ordering = ['introduction_order']
        indexes = [
            models.Index(fields=['milestone', 'importance_weight']),
            models.Index(fields=['milestone', 'introduction_order']),
        ]
        verbose_name = 'Grammar in Milestone'
        verbose_name_plural = 'Grammar in Milestones'
    
    def __str__(self):
        return f"{self.grammar.name} in {self.milestone.name} (order: {self.introduction_order})"


class UserGrammarProgress(models.Model):
    """
    CAPA 4: Tracking de progreso de grammar con SRS (Spaced Repetition)
    
    Mismo algoritmo SM-2 que UserVocabularyProgress
    """
    
    STATUS_CHOICES = [
        ('new', 'Nueva'),
        ('learning', 'Aprendiendo'),
        ('review', 'En repaso'),
        ('mastered', 'Dominada'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='grammar_progress'
    )
    
    grammar = models.ForeignKey(
        GrammarUnit,
        on_delete=models.CASCADE,
        related_name='user_progress'
    )
    
    # ==========================================
    # SRS - Spaced Repetition System (SM-2)
    # ==========================================
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    
    ease_factor = models.FloatField(
        default=2.5,
        help_text='Factor de facilidad (SM-2 algorithm)'
    )
    
    interval = models.PositiveIntegerField(
        default=1,
        help_text='Intervalo en días hasta próximo repaso'
    )
    
    repetitions = models.PositiveIntegerField(
        default=0,
        help_text='Número de repeticiones correctas consecutivas'
    )
    
    # ==========================================
    # TRACKING
    # ==========================================
    next_review = models.DateField(
        default=timezone.now,
        help_text='Fecha del próximo repaso'
    )
    
    last_reviewed = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Última vez que se repasó'
    )
    
    times_correct = models.PositiveIntegerField(
        default=0,
        help_text='Veces que respondió correctamente'
    )
    
    times_incorrect = models.PositiveIntegerField(
        default=0,
        help_text='Veces que respondió incorrectamente'
    )
    
    # ==========================================
    # METADATA
    # ==========================================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_grammar_progress'
        unique_together = ['user', 'grammar']
        ordering = ['next_review', '-updated_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'next_review']),
            models.Index(fields=['grammar', 'status']),
        ]
        verbose_name = 'User Grammar Progress'
        verbose_name_plural = 'User Grammar Progress'
    
    def __str__(self):
        return f"{self.user.username} - {self.grammar.name} ({self.status})"
    
    def process_review(self, quality):
        """
        Procesa el resultado de un repaso usando algoritmo SM-2 y otorga XP.
        
        Args:
            quality (int): Calidad de la respuesta (0-5)
                0: Total blackout
                1: Incorrect pero reconoce
                2: Incorrect pero casi
                3: Correct con esfuerzo
                4: Correct con duda
                5: Correct perfectamente
        """
        from datetime import date
        
        old_status = self.status
        self.last_reviewed = timezone.now()
        
        if quality >= 3:
            # Respuesta correcta
            self.times_correct += 1
            
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)
            
            self.repetitions += 1
            
            # Actualizar ease_factor
            self.ease_factor = self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            
            if self.ease_factor < 1.3:
                self.ease_factor = 1.3
            
            # Actualizar estado
            if self.repetitions >= 3 and self.interval >= 21:
                self.status = 'mastered'
            elif self.repetitions >= 1:
                self.status = 'review'
            else:
                self.status = 'learning'
        
        else:
            # Respuesta incorrecta
            self.times_incorrect += 1
            self.repetitions = 0
            self.interval = 1
            self.status = 'learning'
        
        # Calcular próxima fecha de repaso
        self.next_review = date.today() + timedelta(days=self.interval)
        self.save()
        
        # Award XP via XPService
        cefr_level = getattr(self.grammar, 'level', 'A1') or 'A1'
        
        if quality >= 3:  # Correct review
            XPService.award_word_reviewed_xp(self.user, cefr_level)  # Same XP as vocab review
        
        # Bonus XP for reaching 'mastered' status
        if self.status == 'mastered' and old_status != 'mastered':
            XPService.award_grammar_learned_xp(self.user, cefr_level)
    
    @classmethod
    def get_grammar_for_review(cls, user, limit=10):
        """
        Obtiene grammar units que necesitan repaso hoy
        
        Args:
            user: Usuario
            limit: Número máximo de items
        
        Returns:
            QuerySet de UserGrammarProgress
        """
        from datetime import date
        today = date.today()
        
        return cls.objects.filter(
            user=user,
            next_review__lte=today
        ).select_related('grammar').order_by('next_review')[:limit]
    
    @classmethod
    def get_grammar_stats(cls, user):
        """
        Obtiene estadísticas de grammar del usuario
        
        Returns:
            dict con contadores por status
        """
        from django.db.models import Count
        
        stats = cls.objects.filter(user=user).aggregate(
            total=Count('id'),
            new=Count('id', filter=models.Q(status='new')),
            learning=Count('id', filter=models.Q(status='learning')),
            review=Count('id', filter=models.Q(status='review')),
            mastered=Count('id', filter=models.Q(status='mastered')),
        )
        return stats
