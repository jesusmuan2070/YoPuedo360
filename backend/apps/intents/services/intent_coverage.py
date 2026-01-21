"""
Intent Coverage Map
Define qué intents son relevantes para cada tipo de scenario
"""

# Intents core - SIEMPRE relevantes
CORE_INTENTS = [
    'greet-someone',
    'say-goodbye',
    'thank-someone',
    'apologize',
    'ask-for-help',
    'ask-for-clarification'
]

# Mapeo Intent → Scenarios relevantes
INTENT_SCENARIO_MAP = {
    # Identity intents
    'introduce-self': ['greetings', 'airport', 'hotel', 'work', 'social', 
                       'dating', 'social_media', 'gaming', 'university'],
    'talk-about-origin': ['greetings', 'airport', 'travel', 'social', 'dating'],
    'describe-occupation': ['greetings', 'work', 'networking', 'social', 'dating', 'office'],
    'talk-about-family': ['greetings', 'social', 'home'],
    
    # Needs & Requests
    'ask-for-something': ['restaurant', 'shopping', 'hotel', 'airport', 
                          'transport', 'pharmacy', 'bank'],
    'order-food': ['restaurant', 'cafe', 'airplane', 'hotel', 'cooking'],
    'ask-permission': ['restaurant', 'hotel', 'work', 'social', 'office'],
    
    # Possession & Existence
    'express-possession': ['shopping', 'airport', 'hotel', 'customs', 
                          'home', 'transport', 'pets'],
    'express-existence': ['shopping', 'hotel', 'city', 'directions', 'home'],
    
    # Location
    'ask-where': ['shopping', 'airport', 'hotel', 'city', 'street', 
                  'directions', 'transport', 'university'],
    'describe-location': ['directions', 'city', 'hotel', 'home'],
    
    # Shopping
    'ask-price': ['shopping', 'restaurant', 'market', 'taxi', 'transport', 'salon'],
    'express-quantity': ['shopping', 'restaurant', 'market', 'cooking'],
    'choose-item': ['shopping', 'restaurant', 'market', 'cooking'],
    
    # Time
    'tell-time': ['work', 'appointments', 'travel', 'transport', 'office'],
    'talk-about-daily-routine': ['work', 'social', 'health', 'home', 'gym', 'office'],
    
    # Ability & Preference
    'express-ability': ['work', 'social', 'sports', 'language', 'gaming', 'gym'],
    'express-likes': ['restaurant', 'social', 'hobbies', 'movies', 'music', 
                      'cooking', 'gaming', 'pets', 'dating'],
    
    # Description
    'describe-people': ['social', 'work', 'police', 'dating', 'pets'],
    'describe-objects': ['shopping', 'lost-found', 'police', 'home', 'cooking'],
    
    # Survival
    'make-simple-statement-now': ['work', 'social', 'phone', 'gaming', 'office'],
    'express-simple-opinion': ['restaurant', 'shopping', 'social', 'movies', 
                               'news', 'gaming', 'culture'],
    
    # ========================================
    # A2 INTENTS
    # ========================================
    
    # Past & Time (A2)
    'talk-about-past-experience': ['social', 'work', 'travel', 'university', 'dating'],
    'talk-about-past-habit': ['social', 'work', 'home'],
    'talk-about-past-events': ['social', 'work', 'travel', 'news'],
    'talk-about-dates': ['work', 'appointments', 'travel', 'social'],
    'talk-about-plans': ['social', 'work', 'travel', 'appointments'],
    'talk-about-future-intentions': ['work', 'social', 'university'],
    
    # Daily Life (A2)
    'talk-about-free-time': ['social', 'hobbies', 'sports', 'gym', 'dating'],
    'talk-about-hobbies': ['social', 'sports', 'gaming', 'music', 'cooking'],
    'describe-places': ['travel', 'city', 'hotel', 'directions', 'social'],
    
    # Problems & Complaints (A2)
    'make-simple-complaint': ['restaurant', 'hotel', 'shopping', 'bank', 'phone'],
    'report-a-problem': ['hotel', 'work', 'phone', 'doctor', 'car_rental'],
    'ask-for-solution': ['hotel', 'work', 'phone', 'bank'],
    
    # Shopping & Transactions (A2)
    'compare-items': ['shopping', 'market', 'car_rental'],
    'ask-for-bill': ['restaurant', 'hotel', 'salon'],
    'pay-for-service': ['restaurant', 'hotel', 'salon', 'taxi'],
    
    # Opinion & Preference (A2)
    'express-dislikes': ['restaurant', 'social', 'movies', 'music', 'shopping'],
    'express-obligation': ['work', 'social', 'university', 'home'],
    'give-advice-simple': ['social', 'health', 'doctor', 'gym'],
    'express-preference': ['restaurant', 'shopping', 'social', 'movies'],
    
    # Directions (A2)
    'give-simple-directions': ['city', 'hotel', 'airport', 'directions', 'transport'],
    
    # Social Interaction (A2)
    'make-invitation': ['social', 'dating', 'phone', 'social_media'],
    'accept-invitation': ['social', 'dating', 'phone'],
    'decline-invitation': ['social', 'dating', 'phone'],
    'suggest-activity': ['social', 'dating', 'sports', 'movies'],
    'arrange-meeting': ['work', 'social', 'dating', 'appointments'],
    
    # Communication (A2)
    'ask-someone-to-repeat': ['phone', 'work', 'airport', 'restaurant'],
    'check-understanding': ['work', 'university', 'doctor', 'legal'],
    'correct-mistake': ['work', 'social', 'university'],
    
    # Feelings & Health (A2)
    'express-feelings-basic': ['social', 'health', 'doctor', 'dating'],
    'express-physical-state': ['doctor', 'health', 'pharmacy', 'gym'],
    'describe-symptoms': ['doctor', 'health', 'pharmacy'],
    
    # Information (A2)
    'ask-for-information': ['airport', 'hotel', 'bank', 'doctor', 'university'],
    'give-information': ['work', 'social', 'airport', 'directions'],
    'describe-weather': ['travel', 'social', 'airport'],
    
    # Quantity & Measurement (A2)
    'express-amount': ['shopping', 'cooking', 'restaurant', 'pharmacy'],
    'express-frequency': ['work', 'gym', 'social', 'health'],
    
    # Offers (A2)
    'make-offer': ['social', 'work', 'restaurant', 'dating'],
    'accept-offer': ['social', 'work', 'dating'],
    'refuse-offer': ['social', 'work', 'dating'],
    
    # Additional (A2)
    'express-surprise': ['social', 'news', 'dating', 'gaming'],
    'ask-for-opinion': ['social', 'work', 'restaurant', 'shopping'],
}


def is_intent_relevant(intent, milestone):
    """
    Determina si un intent es relevante para un milestone.
    
    Args:
        intent: CommunicativeIntent instance
        milestone: Milestone instance
        
    Returns:
        bool: True si el intent aplica a este milestone
    """
    scenario_slug = milestone.scenario.slug
    
    # Core intents: siempre relevantes
    if intent.slug in CORE_INTENTS:
        return True
    
    # Buscar en mapa
    if intent.slug in INTENT_SCENARIO_MAP:
        valid_scenarios = INTENT_SCENARIO_MAP[intent.slug]
        
        # Match directo
        if scenario_slug in valid_scenarios:
            return True
        
        # Match parcial (ej: 'restaurant' matchea 'restaurant-fancy')
        for mapped in valid_scenarios:
            if mapped in scenario_slug or scenario_slug in mapped:
                return True
    
    return False
