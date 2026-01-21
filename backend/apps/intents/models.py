"""
Communicative Intents - CEFR A1 Core
Sistema de 3 capas:
1. CommunicativeIntent (abstracto, universal)
2. IntentRealization (concreto, por contexto)  
3. UserIntentProgress (tracking)
"""

from django.db import models
from apps.grammar.models import GrammarUnit
from apps.scenarios.models import Milestone


class CommunicativeIntent(models.Model):
    """
    CAPA 1: Intent PURO - Definición abstracta.
    
    QUÉ puede hacer el usuario (language-agnostic, scenario-agnostic).
    
    Ejemplos:
    - introduce-self
    - order-food
    - ask-price
    
    NO incluye:
    - Frases específicas (van en IntentRealization)
    - Tiempo/dificultad (varía por contexto)
    - Orden rígido (prioridad relativa solamente)
    """
    
    # ==========================================
    # IDENTIDAD
    # ==========================================
    slug = models.SlugField(
        unique=True,
        help_text='Identificador único (ej: introduce-self, order-food)'
    )
    
    name = models.CharField(
        max_length=200,
        help_text='Nombre descriptivo (ej: "Introduce yourself")'
    )
    
    description = models.TextField(
        help_text='Descripción CEFR de la intención comunicativa'
    )
    
    # ==========================================
    # CATEGORÍA CEFR
    # ==========================================
    CATEGORY_CHOICES = [
        ('identity', 'Identity & Personal Info'),
        ('social', 'Social Interaction'),
        ('needs', 'Needs & Requests'),
        ('possession', 'Possession & Existence'),
        ('location', 'Location & Direction'),
        ('shopping', 'Shopping'),
        ('time', 'Time & Routine'),
        ('ability', 'Ability & Preference'),
        ('description', 'Description'),
        ('survival', 'Communication Survival'),
    ]
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        help_text='Categoría CEFR del intent'
    )
    
    # ==========================================
    # NIVEL Y PRIORIDAD
    # ==========================================
    level = models.CharField(
        max_length=2,
        default='A1',
        choices=[
            ('A1', 'A1'),
            ('A2', 'A2'),
            ('B1', 'B1'),
            ('B2', 'B2'),
            ('C1', 'C1'),
            ('C2', 'C2'),
        ],
        help_text='Nivel CEFR'
    )
    
    cefr_rank = models.IntegerField(
        default=3,
        help_text='Ranking de prioridad 1-5 (NO orden absoluto): 1=crítico, 5=opcional'
    )
    
    is_core = models.BooleanField(
        default=True,
        help_text='Si es intent core obligatorio del nivel CEFR'
    )
    
    # ==========================================
    # GRAMMAR GENERAL
    # ==========================================
    # Relación many-to-many con Grammar
    required_grammar = models.ManyToManyField(
        GrammarUnit,
        through='IntentGrammarDependency',
        related_name='supporting_intents',
        blank=True,
        help_text='Grammar típicamente necesaria (puede variar por contexto)'
    )
    
    # ==========================================
    # METADATA
    # ==========================================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'communicative_intent'
        ordering = ['level', 'cefr_rank', 'slug']
        verbose_name = 'Communicative Intent'
        verbose_name_plural = 'Communicative Intents'
        indexes = [
            models.Index(fields=['level', 'cefr_rank']),
            models.Index(fields=['category']),
            models.Index(fields=['is_core']),
        ]
    
    def __str__(self):
        return f"[{self.level}] {self.name}"


class IntentGrammarDependency(models.Model):
    """
    Tabla intermedia: Qué grammar necesita cada intent.
    
    Ejemplo:
    Intent "order-food" necesita:
    - can-infinitive (critical, order=1)
    - countable-uncountable (critical, order=2)
    - articles (optional, order=3)
    """
    
    intent = models.ForeignKey(
        CommunicativeIntent,
        on_delete=models.CASCADE,
        related_name='grammar_dependencies'
    )
    
    grammar = models.ForeignKey(
        GrammarUnit,
        on_delete=models.CASCADE,
        related_name='intent_dependencies'
    )
    
    # ==========================================
    # IMPORTANCIA
    # ==========================================
    is_critical = models.BooleanField(
        default=True,
        help_text='Si es crítica (usuario DEBE aprenderla antes) u opcional'
    )
    
    order = models.IntegerField(
        default=1,
        help_text='Orden de enseñanza dentro del intent (1 primero)'
    )
    
    # ==========================================
    # CONTEXTO
    # ==========================================
    usage_note = models.TextField(
        blank=True,
        help_text='Nota de por qué esta grammar es necesaria para este intent'
    )
    
    class Meta:
        db_table = 'intent_grammar_dependency'
        unique_together = ['intent', 'grammar']
        ordering = ['intent', 'order']
        verbose_name = 'Intent Grammar Dependency'
        verbose_name_plural = 'Intent Grammar Dependencies'
    
    def __str__(self):
        critical = "CRITICAL" if self.is_critical else "optional"
        return f"{self.intent.slug} → {self.grammar.slug} ({critical})"


class IntentRealization(models.Model):
    """
    CAPA 2: Cómo se REALIZA un intent en un milestone específico.
    
    Un intent abstracto → N realizaciones concretas.
    
    Ejemplo:
    Intent "ask-price":
    - En Restaurant: "How much is the coffee?"
    - En Shopping: "How much is this shirt?"
    - En Travel: "How much is the ticket?"
    """
    
    intent = models.ForeignKey(
        CommunicativeIntent,
        on_delete=models.CASCADE,
        related_name='realizations'
    )
    
    milestone = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        related_name='intent_realizations'
    )
    
    # ==========================================
    # EJEMPLOS ESPECÍFICOS DEL CONTEXTO
    # ==========================================
    example_chunks = models.JSONField(
        help_text='Chunks específicos para ESTE contexto: ["Can I have a coffee?", "I\'d like water"]'
    )
    
    example_chunks_es = models.JSONField(
        default=list,
        blank=True,
        help_text='Chunks en español (opcional, para referencia)'
    )
    
    # ==========================================
    # GRAMMAR ADICIONAL (específica del contexto)
    # ==========================================
    additional_grammar = models.ManyToManyField(
        GrammarUnit,
        blank=True,
        help_text='Grammar adicional necesaria en ESTE contexto específico'
    )
    
    # ==========================================
    # METADATA CONTEXTUAL
    # ==========================================
    difficulty = models.IntegerField(
        default=1,
        help_text='Dificultad EN ESTE contexto (1-5)'
    )
    
    estimated_time = models.IntegerField(
        default=10,
        help_text='Tiempo estimado EN ESTE contexto (minutos)'
    )
    
    priority = models.IntegerField(
        default=1,
        help_text='Prioridad dentro de este milestone (1 = más importante)'
    )
    
    is_primary = models.BooleanField(
        default=False,
        help_text='Si este milestone es el PRIMARY para aprender este intent'
    )
    
    # ==========================================
    # METADATA
    # ==========================================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'intent_realization'
        unique_together = ['intent', 'milestone']
        ordering = ['milestone', 'priority']
        indexes = [
            models.Index(fields=['milestone', 'priority']),
            models.Index(fields=['intent', 'is_primary']),
            models.Index(fields=['difficulty']),
        ]
        verbose_name = 'Intent Realization'
        verbose_name_plural = 'Intent Realizations'
    
    def __str__(self):
        primary = "PRIMARY" if self.is_primary else ""
        return f"{self.intent.name} in {self.milestone.name} {primary}"


class UserIntentProgress(models.Model):
    """
    Tracking de progreso del usuario en intents.
    
    Estado del usuario para cada intent:
    - locked: Falta grammar necesaria
    - ready: Grammar completa, listo para practicar
    - practicing: Practicando el intent
    - mastered: Intent dominado
    """
    
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='intent_progress'
    )
    
    intent = models.ForeignKey(
        CommunicativeIntent,
        on_delete=models.CASCADE,
        related_name='user_progress'
    )
    
    # ==========================================
    # ESTADO
    # ==========================================
    STATUS_CHOICES = [
        ('locked', 'Locked - Missing grammar'),
        ('ready', 'Ready to practice'),
        ('practicing', 'Practicing'),
        ('mastered', 'Mastered'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='locked'
    )
    
    # ==========================================
    # PROGRESO DE GRAMMAR
    # ==========================================
    grammar_progress = models.JSONField(
        default=dict,
        help_text='Estado de cada grammar: {"can-infinitive": "mastered", "articles": "learning"}'
    )
    
    # ==========================================
    # MÉTRICAS
    # ==========================================
    times_practiced = models.IntegerField(default=0)
    last_score = models.IntegerField(null=True, blank=True)
    average_score = models.FloatField(null=True, blank=True)
    
    # ==========================================
    # TIMESTAMPS
    # ==========================================
    first_seen_at = models.DateTimeField(auto_now_add=True)
    last_practiced_at = models.DateTimeField(null=True, blank=True)
    mastered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_intent_progress'
        unique_together = ['user', 'intent']
        ordering = ['user', 'intent__cefr_rank']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'intent']),
        ]
        verbose_name = 'User Intent Progress'
        verbose_name_plural = 'User Intent Progress'
    
    def __str__(self):
        return f"{self.user.username} - {self.intent.name} ({self.status})"
