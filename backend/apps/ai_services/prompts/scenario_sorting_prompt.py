"""
Scenario Ranking Prompt
Used by ARIA to rank scenarios based on user profile
"""

from typing import List, Dict, Any


SCENARIO_RANKING_SYSTEM = """You are an AI assistant for a language learning app.
Your task is to rank learning scenarios based on user preferences.
Always respond in valid JSON format."""


SCENARIO_SORTING_PROMPT = """
Given this user profile:
- CEFR Level: {cefr_level}
- Learning Goals: {goals}
- Interests: {interests}
- Work Domain: {work_domain}
- Profession: {profession}
- Hobbies: {hobbies}

Rank these {num_scenarios} language learning scenarios from MOST to LEAST relevant for this user.
Consider:
1. Their profession and work domain (prioritize work-related scenarios for professionals)
2. Their personal interests and hobbies
3. Their learning goals
4. Scenarios that would be immediately useful in their daily life

Available scenarios:
{scenarios_list}

Return a JSON object with this format:
{{
  "ranked_ids": [id1, id2, id3, ...],
  "top_5_reasoning": [
    {{"id": id1, "reason": "brief reason why this is #1"}},
    {{"id": id2, "reason": "brief reason why this is #2"}},
    ...
  ]
}}

Only include scenario IDs that exist in the list. Return ALL IDs in ranked order.
"""


def format_scenario_ranking_prompt(
    user_profile: Dict[str, Any],
    scenarios: List[Dict[str, Any]]
) -> str:
    """
    Format the scenario ranking prompt with user data.
    
    Args:
        user_profile: User's learning profile data
        scenarios: List of scenario dicts with 'id', 'name', 'tags'
    
    Returns:
        Formatted prompt string
    """
    # Format goals nicely
    goals = user_profile.get('goals', {})
    if goals:
        goals_str = ', '.join([
            f"{g} ({int(w*100)}%)" for g, w in goals.items()
        ])
    else:
        goals_str = "Not specified"
    
    # Format interests
    interests = user_profile.get('interests', {})
    if interests:
        interests_str = ', '.join(interests.keys())
    else:
        interests_str = "Not specified"
    
    # Format hobbies
    hobbies = user_profile.get('hobbies', [])
    hobbies_str = ', '.join(hobbies) if hobbies else "Not specified"
    
    # Format scenarios list
    scenarios_lines = []
    for s in scenarios:
        tags_str = ', '.join(s.get('tags', []))
        scenarios_lines.append(f"- ID {s['id']}: {s['name']} (tags: {tags_str})")
    
    return SCENARIO_SORTING_PROMPT.format(
        cefr_level=user_profile.get('cefr_level', 'A1'),
        goals=goals_str,
        interests=interests_str,
        work_domain=user_profile.get('work_domain', 'Not specified'),
        profession=user_profile.get('profession', 'Not specified'),
        hobbies=hobbies_str,
        num_scenarios=len(scenarios),
        scenarios_list='\n'.join(scenarios_lines)
    )
