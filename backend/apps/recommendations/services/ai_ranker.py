"""
AI Ranker Service
Uses OpenAI to intelligently rank scenarios based on user profile
"""

from typing import List, Dict, Any
from apps.scenarios.models import Scenario
from apps.ai_services.clients.openai_client import OpenAIClient
from apps.ai_services.prompts.scenario_ranking import (
    SCENARIO_RANKING_SYSTEM,
    format_scenario_ranking_prompt
)
from .base import BaseRecommender


class AIRanker(BaseRecommender):
    """
    Uses AI to rank scenarios based on user profile.
    Considers profession, interests, hobbies, and goals intelligently.
    """
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self._client = None
    
    @property
    def name(self) -> str:
        return "AIRanker"
    
    @property
    def client(self) -> OpenAIClient:
        if self._client is None:
            self._client = OpenAIClient(model=self.model)
        return self._client
    
    def process(self, scenarios: List[Scenario], user_profile: Dict[str, Any]) -> List[Scenario]:
        """
        Rank scenarios using AI.
        
        Args:
            scenarios: List of scenarios to rank
            user_profile: User's learning profile
        
        Returns:
            Scenarios ordered by AI-determined relevance
        """
        if not scenarios:
            return scenarios
        
        # Prepare scenarios data for prompt
        scenarios_data = []
        scenario_map = {}
        
        for s in scenarios:
            tags = [t.value for t in s.tags.all()]
            scenarios_data.append({
                'id': s.id,
                'name': s.name,
                'tags': tags
            })
            scenario_map[s.id] = s
        
        # Get AI ranking
        try:
            ranked_ids = self._get_ai_ranking(user_profile, scenarios_data)
            
            # Reorder scenarios based on AI ranking
            ranked_scenarios = []
            for sid in ranked_ids:
                if sid in scenario_map:
                    ranked_scenarios.append(scenario_map[sid])
            
            # Add any scenarios not in AI response at the end
            ranked_set = set(ranked_ids)
            for s in scenarios:
                if s.id not in ranked_set:
                    ranked_scenarios.append(s)
            
            return ranked_scenarios
            
        except Exception as e:
            print(f"AIRanker error: {e}")
            # Fallback to original order
            return scenarios
    
    def _get_ai_ranking(
        self,
        user_profile: Dict[str, Any],
        scenarios_data: List[Dict[str, Any]]
    ) -> List[int]:
        """Get ranked scenario IDs from AI."""
        
        prompt = format_scenario_ranking_prompt(user_profile, scenarios_data)
        
        response = self.client.complete_json(
            prompt=prompt,
            system_prompt=SCENARIO_RANKING_SYSTEM,
            temperature=0.3,
            max_tokens=1000
        )
        
        # Extract ranked IDs
        ranked_ids = response.get('ranked_ids', [])
        
        # Log reasoning for debugging
        if 'top_5_reasoning' in response:
            for item in response['top_5_reasoning'][:3]:
                print(f"  AI: #{item.get('id')} - {item.get('reason')}")
        
        return ranked_ids
