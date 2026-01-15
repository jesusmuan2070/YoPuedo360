"""
Level Filter
Filters scenarios by user's CEFR level
"""

from typing import List, Dict, Any
from apps.scenarios.models import Scenario
from .base import BaseRecommender


class LevelFilter(BaseRecommender):
    """
    Filters scenarios to match user's CEFR level.
    Returns only scenarios that are at or below the user's skill level.
    """
    
    # CEFR level order for comparison
    CEFR_ORDER = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    
    @property
    def name(self) -> str:
        return "LevelFilter"
    
    def process(self, scenarios: List[Scenario], user_profile: Dict[str, Any]) -> List[Scenario]:
        """
        Filter scenarios by CEFR level.
        
        Args:
            scenarios: All available scenarios
            user_profile: Must contain 'cefr_level' (e.g., 'A1', 'B2')
        
        Returns:
            Scenarios at or below user's level
        """
        user_level = user_profile.get('cefr_level', 'A1')
        user_level_index = self._get_level_index(user_level)
        
        filtered = []
        for scenario in scenarios:
            # Use scenario's min_level if available, otherwise include all
            scenario_level = getattr(scenario, 'min_level', None)
            if scenario_level:
                if self._get_level_index(scenario_level) <= user_level_index:
                    filtered.append(scenario)
            else:
                # If no level specified, include for all users
                filtered.append(scenario)
        
        return filtered
    
    def _get_level_index(self, level: str) -> int:
        """Convert CEFR level to numeric index for comparison."""
        try:
            return self.CEFR_ORDER.index(level.upper())
        except (ValueError, AttributeError):
            return 0  # Default to A1 if invalid
