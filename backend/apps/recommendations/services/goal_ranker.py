"""
Goal Ranker
Ranks scenarios based on user's learning goals with weights
"""

from typing import List, Dict, Any, Tuple
from apps.scenarios.models import Scenario
from .base import BaseRecommender


class GoalRanker(BaseRecommender):
    """
    Ranks scenarios based on how well they match user's goals.
    Uses goal weights (e.g., work: 0.7, travel: 0.3) for scoring.
    """
    
    @property
    def name(self) -> str:
        return "GoalRanker"
    
    @property
    def weight(self) -> float:
        return 0.7  # Goals have 70% weight in final score
    
    def process(self, scenarios: List[Scenario], user_profile: Dict[str, Any]) -> List[Scenario]:
        """
        Rank scenarios by goal match.
        
        Args:
            scenarios: Filtered scenarios
            user_profile: Must contain 'goals' dict (e.g., {'work': 0.7, 'travel': 0.3})
        
        Returns:
            Scenarios sorted by goal match score (highest first)
        """
        user_goals = user_profile.get('goals', {})
        
        if not user_goals:
            return scenarios
        
        # Calculate score for each scenario
        scored: List[Tuple[Scenario, float]] = []
        
        for scenario in scenarios:
            score = self._calculate_goal_score(scenario, user_goals)
            scored.append((scenario, score))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return [s for s, _ in scored]
    
    def _calculate_goal_score(self, scenario: Scenario, user_goals: Dict[str, float]) -> float:
        """
        Calculate how well scenario matches user's goals.
        
        Returns score from 0.0 to 1.0
        """
        scenario_tags = set(
            tag.value for tag in scenario.tags.filter(type='goal')
        )
        
        if not scenario_tags:
            return 0.0
        
        total_score = 0.0
        
        for goal, weight in user_goals.items():
            if goal in scenario_tags:
                total_score += weight
        
        return total_score
