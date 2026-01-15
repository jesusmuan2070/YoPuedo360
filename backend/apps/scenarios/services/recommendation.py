"""
Recommendation Service - ENGAGEMENT-FIRST Algorithm
Calculates priority scores for scenarios based on user profile.
"""

from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from typing import List, Dict, Any

from apps.scenarios.models import Scenario, UserScenarioProgress, Tag
from apps.users.models import LearningProfile


class RecommendationService:
    """
    Servicio de recomendación de escenarios.
    Implementa el algoritmo ENGAGEMENT-FIRST.
    
    score = (
        goal_match * 3        # Relevancia (30%)
      + interest_match * 2    # Motivación (20%)  
      + engagement_boost * 3  # ENGAGEMENT (30%)
      + novelty * 1           # Curiosidad (10%)
      + level_adjustment      # Dificultad (10%)
      - fatigue_penalty       # Evitar aburrimiento
    )
    """
    
    # Pesos del algoritmo
    WEIGHT_GOAL = 3
    WEIGHT_INTEREST = 2
    WEIGHT_ENGAGEMENT = 3
    WEIGHT_NOVELTY = 1
    WEIGHT_LEVEL = 1
    WEIGHT_FATIGUE = 1
    
    def __init__(self, user):
        self.user = user
        self.profile = self._get_profile()
        self.history = self._get_history()
    
    def _get_profile(self) -> Dict:
        """Obtiene el perfil de aprendizaje del usuario"""
        try:
            lp = self.user.learning_profile
            return {
                'level': lp.cefr_level,
                'goals': lp.goals or {},
                'interests': lp.interests or {},
                'work_domain': lp.work_domain,
                'streak': lp.streak_days,
                'time_per_day': lp.daily_goal_minutes,
            }
        except LearningProfile.DoesNotExist:
            return {
                'level': 'A1',
                'goals': {},
                'interests': {},
                'work_domain': '',
                'streak': 0,
                'time_per_day': 15,
            }
    
    def _get_history(self) -> Dict:
        """Obtiene el historial del usuario"""
        # Escenarios completados
        completed = UserScenarioProgress.objects.filter(
            user=self.user,
            is_completed=True
        ).values_list('scenario__slug', flat=True)
        
        # Escenarios recientes (últimos 3 días)
        recent = UserScenarioProgress.objects.filter(
            user=self.user,
            last_activity__gte=timezone.now() - timedelta(days=3)
        ).select_related('scenario').order_by('-last_activity')[:5]
        
        return {
            'completed': list(completed),
            'recent': [p.scenario for p in recent],
            'domains_today': self._get_domains_today(),
        }
    
    def _get_domains_today(self) -> set:
        """Dominios practicados hoy"""
        today = timezone.now().date()
        today_scenarios = UserScenarioProgress.objects.filter(
            user=self.user,
            last_activity__date=today
        ).select_related('scenario')
        
        domains = set()
        for progress in today_scenarios:
            for tag in progress.scenario.tags.filter(type='domain'):
                domains.add(tag.value)
        return domains
    
    def get_recommended_scenarios(self, limit: int = 10) -> List[Dict]:
        """
        Obtiene escenarios recomendados ordenados por score.
        """
        # Filtrar escenarios por nivel
        scenarios = Scenario.objects.filter(
            is_active=True,
            difficulty_min__lte=self.profile['level'],
        ).prefetch_related('tags')
        
        # Calcular score para cada escenario
        scored = []
        for scenario in scenarios:
            score = self.calculate_priority(scenario)
            scored.append({
                'scenario': scenario,
                'score': score,
            })
        
        # Ordenar por score
        scored.sort(key=lambda x: x['score'], reverse=True)
        
        # Alternar dominios para variedad
        result = self._alternate_domains(scored)
        
        return result[:limit]
    
    def calculate_priority(self, scenario: Scenario) -> float:
        """
        Calcula el score de prioridad para un escenario.
        """
        score = 0.0
        
        # 1. Goal match (30%)
        score += self._calculate_goal_match(scenario) * self.WEIGHT_GOAL
        
        # 2. Interest match (20%)
        score += self._calculate_interest_match(scenario) * self.WEIGHT_INTEREST
        
        # 3. Engagement boost (30%)
        score += self._calculate_engagement_boost(scenario) * self.WEIGHT_ENGAGEMENT
        
        # 4. Novelty (10%)
        score += self._calculate_novelty(scenario) * self.WEIGHT_NOVELTY
        
        # 5. Level adjustment (10%)
        score += self._calculate_level_adjustment(scenario) * self.WEIGHT_LEVEL
        
        # 6. Fatigue penalty
        score -= self._calculate_fatigue_penalty(scenario) * self.WEIGHT_FATIGUE
        
        return round(score, 2)
    
    def _calculate_goal_match(self, scenario: Scenario) -> float:
        """Match con metas del usuario"""
        match = 0.0
        scenario_goals = set(scenario.tags.filter(type='goal').values_list('value', flat=True))
        
        for goal, weight in self.profile['goals'].items():
            if goal in scenario_goals:
                match += weight
        
        # Bonus por work_domain
        if self.profile['work_domain']:
            work_domains = set(scenario.tags.filter(type='work_domain').values_list('value', flat=True))
            if self.profile['work_domain'] in work_domains:
                match += 0.5
        
        return match
    
    def _calculate_interest_match(self, scenario: Scenario) -> float:
        """Match con intereses del usuario"""
        match = 0.0
        scenario_domains = set(scenario.tags.filter(type='domain').values_list('value', flat=True))
        scenario_interests = set(scenario.tags.filter(type='interest').values_list('value', flat=True))
        all_scenario_tags = scenario_domains | scenario_interests
        
        for interest, weight in self.profile['interests'].items():
            if interest in all_scenario_tags:
                match += weight
        
        return match
    
    def _calculate_engagement_boost(self, scenario: Scenario) -> float:
        """
        Factores de engagement:
        - Streak bonus
        - Milestone cercano
        - Quick win
        - Variedad de dominio
        """
        boost = 0.0
        
        # Streak bonus
        if self.profile['streak'] >= 3:
            boost += 0.3
        if self.profile['streak'] >= 7:
            boost += 0.2
        
        # Quick win (escenario con milestone corto cuando poco tiempo)
        if self.profile['time_per_day'] <= 10:
            first_milestone = scenario.milestones.filter(
                level=self.profile['level']
            ).first()
            if first_milestone and first_milestone.estimated_time <= 5:
                boost += 0.5
        
        # Variedad de dominio (nuevo dominio hoy)
        scenario_domains = set(scenario.tags.filter(type='domain').values_list('value', flat=True))
        if not scenario_domains & self.history['domains_today']:
            boost += 0.3
        
        return boost
    
    def _calculate_novelty(self, scenario: Scenario) -> float:
        """Bonus si el escenario no está completado"""
        if scenario.slug not in self.history['completed']:
            return 1.0
        return 0.0
    
    def _calculate_level_adjustment(self, scenario: Scenario) -> float:
        """Ajuste por dificultad apropiada"""
        level_order = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        
        try:
            user_idx = level_order.index(self.profile['level'])
            min_idx = level_order.index(scenario.difficulty_min)
            max_idx = level_order.index(scenario.difficulty_max)
        except ValueError:
            return 0.0
        
        # Perfecto si nivel está en rango
        if min_idx <= user_idx <= max_idx:
            return 0.5
        
        # Penaliza si está muy lejos
        distance = min(abs(user_idx - min_idx), abs(user_idx - max_idx))
        return -0.3 * distance
    
    def _calculate_fatigue_penalty(self, scenario: Scenario) -> float:
        """Penaliza dominios/skills repetidos recientemente"""
        penalty = 0.0
        
        scenario_domains = set(scenario.tags.filter(type='domain').values_list('value', flat=True))
        scenario_skills = set(scenario.tags.filter(type='skill').values_list('value', flat=True))
        
        for recent in self.history['recent'][:3]:
            recent_domains = set(recent.tags.filter(type='domain').values_list('value', flat=True))
            recent_skills = set(recent.tags.filter(type='skill').values_list('value', flat=True))
            
            if scenario_domains & recent_domains:
                penalty += 0.3
            if scenario_skills & recent_skills:
                penalty += 0.15
        
        return penalty
    
    def _alternate_domains(self, scored: List[Dict]) -> List[Dict]:
        """Reordena para evitar repetir dominios seguidos"""
        if not scored:
            return scored
        
        result = []
        used_domains = set()
        remaining = scored.copy()
        
        while remaining:
            # Buscar siguiente escenario con dominio diferente
            found = False
            for i, item in enumerate(remaining):
                scenario_domains = set(
                    item['scenario'].tags.filter(type='domain').values_list('value', flat=True)
                )
                
                if not scenario_domains & used_domains or len(remaining) <= 2:
                    result.append(item)
                    used_domains = scenario_domains
                    remaining.pop(i)
                    found = True
                    break
            
            if not found:
                # Si no hay diferente, tomar el primero
                result.append(remaining.pop(0))
        
        return result


def get_recommendations(user, limit=10) -> List[Dict]:
    """
    Función helper para obtener recomendaciones.
    Uso: recommendations = get_recommendations(request.user)
    """
    service = RecommendationService(user)
    return service.get_recommended_scenarios(limit=limit)
