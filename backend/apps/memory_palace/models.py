"""
Memory Palace Models - Scenarios, Tags, Milestones
Core models for the personalized learning system
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    """
    Sistema de categorización flexible.
    Permite filtrar y ordenar escenarios según preferencias del usuario.
    """
    TYPE_CHOICES = [
        ('goal', 'Goal'),           # work, travel, personal, certification
        ('domain', 'Domain'),       # food, business, health, entertainment
        ('skill', 'Skill'),         # speaking, listening, reading, writing
        ('work_domain', 'Work Domain'),  # tech, sales, health, education
        ('interest', 'Interest'),   # gaming, music, sports, cinema
    ]
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, db_index=True)
    value = models.CharField(max_length=50)
    display_name = models.CharField(max_length=100, blank=True)
    icon = models.CharField(max_length=10, blank=True)  # emoji
    
    class Meta:
        unique_together = ['type', 'value']
        ordering = ['type', 'value']
    
    def __str__(self):
        return f"{self.type}:{self.value}"
    
    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.value.replace('_', ' ').title()
        super().save(*args, **kwargs)


class Scenario(models.Model):
    """
    Escenario de vida real (restaurante, oficina, aeropuerto, etc.)
    Cada escenario tiene milestones adaptados a cada nivel CEFR.
    """
    DIFFICULTY_CHOICES = [
        ('A1', 'A1 - Principiante'),
        ('A2', 'A2 - Básico'),
        ('B1', 'B1 - Intermedio'),
        ('B2', 'B2 - Intermedio Alto'),
        ('C1', 'C1 - Avanzado'),
        ('C2', 'C2 - Maestría'),
    ]
    
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)  # emoji
    description = models.TextField()
    image_url = models.URLField(blank=True)
    
    # Rango de dificultad
    difficulty_min = models.CharField(max_length=2, choices=DIFFICULTY_CHOICES, default='A1')
    difficulty_max = models.CharField(max_length=2, choices=DIFFICULTY_CHOICES, default='C2')
    
    # Tags para el algoritmo de recomendación
    tags = models.ManyToManyField(Tag, related_name='scenarios')
    
    # Metadata
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.icon} {self.name}"
    
    def get_milestones_for_level(self, level):
        """Retorna milestones filtrados por nivel"""
        return self.milestones.filter(level=level).order_by('order')
    
    def get_tags_by_type(self, tag_type):
        """Retorna tags de un tipo específico"""
        return self.tags.filter(type=tag_type)


class Milestone(models.Model):
    """
    Objetivo de aprendizaje dentro de un escenario.
    Cada milestone está adaptado a un nivel CEFR específico.
    Ejemplo: "Pedir una mesa" (A1), "Hacer una queja" (B1)
    """
    scenario = models.ForeignKey(
        Scenario, 
        on_delete=models.CASCADE, 
        related_name='milestones'
    )
    level = models.CharField(max_length=2, choices=Scenario.DIFFICULTY_CHOICES)
    order = models.PositiveIntegerField()
    
    name = models.CharField(max_length=100)  # "Pedir una mesa"
    description = models.TextField(blank=True)
    objectives = models.JSONField(default=list)  # ["Saludar al mesero", "Decir número de personas"]
    
    # Tiempo estimado en minutos
    estimated_time = models.PositiveIntegerField(default=10)
    
    # Cuántas palabras nuevas introduce este milestone
    new_vocab_count = models.PositiveIntegerField(default=20)
    
    class Meta:
        unique_together = ['scenario', 'level', 'order']
        ordering = ['scenario', 'level', 'order']
    
    def __str__(self):
        return f"{self.scenario.name} - {self.level} - {self.name}"


class UserScenarioProgress(models.Model):
    """
    Progreso del usuario en cada escenario.
    Trackea qué milestones ha completado.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scenario_progress')
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    
    # Milestone actual (el siguiente a completar)
    current_milestone = models.ForeignKey(
        Milestone, 
        null=True, 
        blank=True,
        on_delete=models.SET_NULL
    )
    
    # Estado
    is_started = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    
    # Tracking
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    # Score/engagement
    total_time_spent = models.PositiveIntegerField(default=0)  # segundos
    stars_earned = models.PositiveIntegerField(default=0)  # 0-3
    
    class Meta:
        unique_together = ['user', 'scenario']
    
    def __str__(self):
        status = "✅" if self.is_completed else "🔄" if self.is_started else "⬜"
        return f"{status} {self.user.username} - {self.scenario.name}"
    
    def get_progress_percentage(self):
        """Calcula el porcentaje de progreso"""
        if not self.current_milestone:
            return 0 if not self.is_completed else 100
        
        total = self.scenario.milestones.filter(level=self.current_milestone.level).count()
        completed = self.current_milestone.order - 1
        return int((completed / total) * 100) if total > 0 else 0
