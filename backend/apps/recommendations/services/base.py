"""
Base Recommender Interface
Abstract base class for all recommender components
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from apps.scenarios.models import Scenario


class BaseRecommender(ABC):
    """
    Abstract base class for recommendation components.
    Each component implements one specific ranking/filtering logic.
    """
    
    @abstractmethod
    def process(self, scenarios: List[Scenario], user_profile: Dict[str, Any]) -> List[Scenario]:
        """
        Process scenarios and return filtered/ranked list.
        
        Args:
            scenarios: List of Scenario objects to process
            user_profile: Dict with user preferences (goals, interests, level, etc.)
        
        Returns:
            Processed list of Scenario objects
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of this recommender component."""
        pass
    
    @property
    def weight(self) -> float:
        """
        Weight of this component in the final score (0.0 to 1.0).
        Override in subclasses if needed.
        """
        return 1.0
