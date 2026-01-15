"""
Recommendation Engine - ARIA
Adaptive Recommendation Intelligence Algorithm

Main orchestrator that combines all recommendation components.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from apps.memory_palace.models import Scenario
from apps.users.models import LearningProfile

from .level_filter import LevelFilter
from .ai_ranker import AIRanker


@dataclass
class RecommendationResult:
    """Result of a recommendation request."""
    scenarios: List[Scenario]
    total_count: int
    user_level: str
    applied_filters: List[str]


class RecommendationEngine:
    """
    ARIA - Adaptive Recommendation Intelligence Algorithm
    
    Orchestrates the recommendation pipeline:
    1. Level Filter - Filter by CEFR level
    2. AI Ranker - Intelligent ranking using OpenAI
    
    Usage:
        engine = RecommendationEngine()
        result = engine.recommend(user)
        
        # Or without AI (faster, cheaper)
        engine = RecommendationEngine(use_ai=False)
    """
    
    def __init__(self, use_ai: bool = True, ai_model: str = "gpt-4o-mini"):
        self.use_ai = use_ai
        self.level_filter = LevelFilter()
        
        if use_ai:
            self.ai_ranker = AIRanker(model=ai_model)
        else:
            self.ai_ranker = None
    
    def recommend(
        self,
        user,
        limit: int = 10,
        include_completed: bool = False,
        discovery_slots: int = 2,
    ) -> RecommendationResult:
        """
        Get personalized scenario recommendations for a user.
        Uses cached results when available to avoid repeated OpenAI calls.
        """
        import random
        import hashlib
        import json
        from datetime import date
        from apps.progress.models import UserMilestoneProgress
        from apps.recommendations.models import UserOrderedScenarios
        
        profile = self._get_user_profile(user)
        applied_filters = ['cached']
        
        # Calculate profile hash to detect changes
        profile_hash = hashlib.md5(
            json.dumps(profile, sort_keys=True).encode()
        ).hexdigest()
        
        # Try to get cached recommendations
        cache, created = UserOrderedScenarios.objects.get_or_create(user=user)
        
        # Check if we need to regenerate (no cache or profile changed)
        if not cache.scenario_order or cache.profile_hash != profile_hash:
            # Generate fresh recommendations (calls OpenAI)
            fresh_result = self._generate_fresh_recommendations(user, profile)
            
            # Save to cache
            cache.scenario_order = [s.id for s in fresh_result.scenarios]
            cache.user_level = fresh_result.user_level
            cache.profile_hash = profile_hash
            cache.save()
            
            applied_filters = fresh_result.applied_filters + ['newly_cached']
            ordered_ids = cache.scenario_order
        else:
            ordered_ids = cache.scenario_order
        
        # Load scenarios in cached order
        all_scenarios = {s.id: s for s in Scenario.objects.filter(is_active=True)}
        scenarios = [all_scenarios[sid] for sid in ordered_ids if sid in all_scenarios]
        
        # Get scenarios where user has progress
        scenarios_with_progress = set(
            UserMilestoneProgress.objects.filter(user=user)
            .values_list('milestone__scenario_id', flat=True)
        )
        
        total_count = len(scenarios)
        
        # Add discovery slots (rotates daily)
        if discovery_slots > 0 and limit > discovery_slots:
            from datetime import date
            
            main_limit = limit - discovery_slots
            main_scenarios = scenarios[:main_limit]
            main_scenario_ids = {s.id for s in main_scenarios}
            
            # Separate candidates: untouched vs with progress
            untouched_candidates = []
            progress_candidates = []
            
            for s in scenarios[main_limit:]:
                if s.id in main_scenario_ids:
                    continue
                if s.id in scenarios_with_progress:
                    progress_candidates.append(s)  # User started this - keep it
                else:
                    untouched_candidates.append(s)
            
            # Daily seed = consistent rotation throughout the day
            # Uses user.id to give each user different discovery slots
            today_seed = int(date.today().strftime('%Y%m%d')) + user.id
            random.seed(today_seed)
            random.shuffle(untouched_candidates)
            random.seed()  # Reset to true random
            
            discovery_scenarios = []
            
            # Priority 1: Scenarios with progress (user already started)
            discovery_scenarios.extend(progress_candidates[:discovery_slots])
            
            # Priority 2: Fill remaining slots with untouched (daily rotation)
            remaining_slots = discovery_slots - len(discovery_scenarios)
            if remaining_slots > 0:
                discovery_scenarios.extend(untouched_candidates[:remaining_slots])
            
            final_scenarios = main_scenarios + discovery_scenarios
            applied_filters.append(f"discovery_slots:{discovery_slots}:daily")
        else:
            final_scenarios = scenarios[:limit]
        
        return RecommendationResult(
            scenarios=final_scenarios,
            total_count=total_count,
            user_level=profile.get('cefr_level', 'A1'),
            applied_filters=applied_filters
        )
    
    def _get_user_profile(self, user) -> Dict[str, Any]:
        """Extract user profile data for recommendation."""
        try:
            profile = LearningProfile.objects.get(user=user)
            return {
                'cefr_level': profile.cefr_level or 'A1',
                'goals': profile.goals or {},
                'interests': profile.interests or {},
                'work_domain': profile.work_domain or '',
                'profession': profile.profession or '',
                'hobbies': profile.hobbies or [],
            }
        except LearningProfile.DoesNotExist:
            return {
                'cefr_level': 'A1',
                'goals': {},
                'interests': {},
                'work_domain': '',
                'profession': '',
                'hobbies': [],
            }
    
    def _generate_fresh_recommendations(self, user, profile: Dict = None) -> RecommendationResult:
        """
        Generate fresh recommendations using OpenAI.
        Called only when cache is missing or profile changed.
        """
        if profile is None:
            profile = self._get_user_profile(user)
        
        # Get all active scenarios
        scenarios = list(Scenario.objects.filter(is_active=True).prefetch_related('tags'))
        
        applied_filters = []
        
        # Step 1: Filter by level
        scenarios = self.level_filter.process(scenarios, profile)
        applied_filters.append(self.level_filter.name)
        
        # Step 2: AI Ranking (if enabled)
        if self.use_ai and self.ai_ranker:
            scenarios = self.ai_ranker.process(scenarios, profile)
            applied_filters.append(self.ai_ranker.name)
        
        return RecommendationResult(
            scenarios=scenarios,
            total_count=len(scenarios),
            user_level=profile.get('cefr_level', 'A1'),
            applied_filters=applied_filters
        )
    
    def get_similar_scenarios(self, scenario: Scenario, limit: int = 5) -> List[Scenario]:
        """
        Get scenarios similar to the given one.
        Based on shared tags.
        """
        scenario_tags = set(scenario.tags.values_list('id', flat=True))
        
        similar = []
        all_scenarios = Scenario.objects.filter(is_active=True).exclude(id=scenario.id)
        
        for s in all_scenarios:
            s_tags = set(s.tags.values_list('id', flat=True))
            overlap = len(scenario_tags & s_tags)
            if overlap > 0:
                similar.append((s, overlap))
        
        similar.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in similar[:limit]]
