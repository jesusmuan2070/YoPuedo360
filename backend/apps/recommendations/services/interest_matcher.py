"""
Interest Matcher
Boosts scenarios that match user's interests
"""

from typing import List, Dict, Any, Tuple
from apps.memory_palace.models import Scenario
from .base import BaseRecommender


class InterestMatcher(BaseRecommender):
    """
    Boosts scenario rankings based on interest matches.
    Interests have equal weight, so any match gets a boost.
    """
    
    @property
    def name(self) -> str:
        return "InterestMatcher"
    
    @property
    def weight(self) -> float:
        return 0.2  # Interests have 20% weight in final score
    
    def process(self, scenarios: List[Scenario], user_profile: Dict[str, Any]) -> List[Scenario]:
        """
        Boost scenarios that match user interests.
        
        Args:
            scenarios: Scenarios (already ranked by goals)
            user_profile: Must contain 'interests' dict
        
        Returns:
            Scenarios with interest-matched ones boosted
        """
        user_interests = user_profile.get('interests', {})
        
        if not user_interests:
            return scenarios
        
        interest_keys = set(user_interests.keys())
        
        # Calculate interest score for each scenario
        scored: List[Tuple[Scenario, float, int]] = []
        
        for idx, scenario in enumerate(scenarios):
            interest_score = self._calculate_interest_score(scenario, interest_keys)
            # Preserve original order as tiebreaker
            scored.append((scenario, interest_score, idx))
        
        # Sort by interest score, then by original position
        scored.sort(key=lambda x: (-x[1], x[2]))
        
        return [s for s, _, _ in scored]
    
    def _calculate_interest_score(self, scenario: Scenario, user_interests: set) -> float:
        """
        Calculate interest match score.
        
        Returns number of matching interests (0.0 to 1.0 normalized)
        """
        scenario_domains = set(
            tag.value for tag in scenario.tags.filter(type__in=['domain', 'interest'])
        )
        
        if not scenario_domains:
            return 0.0
        
        matches = len(scenario_domains & user_interests)
        
        # Normalize by number of user interests
        if len(user_interests) > 0:
            return matches / len(user_interests)
        
        return 0.0
