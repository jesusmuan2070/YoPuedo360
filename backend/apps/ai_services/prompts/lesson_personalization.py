"""
Lesson Personalization Prompt
Used to customize lesson content based on user profile
"""

from typing import Dict, Any


LESSON_PERSONALIZATION_SYSTEM = """You are an AI assistant for a language learning app.
Your task is to personalize lesson content based on user profile.
Create engaging, relevant examples using the user's profession and interests.
Always respond in valid JSON format."""


LESSON_PERSONALIZATION_PROMPT = """
Personalize this lesson for the user:

User Profile:
- Profession: {profession}
- Work Domain: {work_domain}
- Interests: {interests}
- Hobbies: {hobbies}
- Native Language: {native_language}
- Target Language: {target_language}
- CEFR Level: {cefr_level}

Lesson to personalize:
- Scenario: {scenario_name}
- Topic: {topic}
- Original Vocabulary: {vocabulary}
- Original Phrases: {phrases}

Create personalized versions that relate to the user's profession and interests.
For a {profession} interested in {interests}, use relevant examples.

Return JSON:
{{
  "personalized_vocabulary": [
    {{"word": "...", "translation": "...", "example": "contextual example for this user"}}
  ],
  "personalized_phrases": [
    {{"phrase": "...", "translation": "...", "context": "when the user would use this"}}
  ],
  "personalized_dialogue": {{
    "situation": "realistic scenario for this user",
    "lines": [{{"speaker": "A/B", "text": "..."}}]
  }}
}}
"""


def format_lesson_personalization_prompt(
    user_profile: Dict[str, Any],
    lesson_data: Dict[str, Any]
) -> str:
    """Format the lesson personalization prompt."""
    
    interests = user_profile.get('interests', {})
    interests_str = ', '.join(interests.keys()) if interests else "general"
    
    hobbies = user_profile.get('hobbies', [])
    hobbies_str = ', '.join(hobbies) if hobbies else "none specified"
    
    return LESSON_PERSONALIZATION_PROMPT.format(
        profession=user_profile.get('profession', 'general'),
        work_domain=user_profile.get('work_domain', 'general'),
        interests=interests_str,
        hobbies=hobbies_str,
        native_language=user_profile.get('native_language', 'es'),
        target_language=user_profile.get('target_language', 'en'),
        cefr_level=user_profile.get('cefr_level', 'A1'),
        scenario_name=lesson_data.get('scenario_name', ''),
        topic=lesson_data.get('topic', ''),
        vocabulary=lesson_data.get('vocabulary', []),
        phrases=lesson_data.get('phrases', [])
    )
