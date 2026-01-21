"""
Seed CEFR A1 Communicative Intents - SIMPLIFIED
Solo intents puros, sin ejemplos ni metadata contextual.

Run with: python scripts/seed_intents_a1_simple.py
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
django.setup()

from apps.intents.models import CommunicativeIntent

print("🎯 Seeding CEFR A1 Communicative Intents (28 core - simplified)...\n")

# ============================================
# 28 INTENTS CORE A1 - SOLO DEFINICIÓN
# ============================================

INTENTS_A1 = [
    # Identity & Personal Info
    {'slug': 'introduce-self', 'name': 'Introduce yourself', 'category': 'identity', 'cefr_rank': 1},
    {'slug': 'talk-about-origin', 'name': 'Talk about where you\'re from', 'category': 'identity', 'cefr_rank': 1},
    {'slug': 'describe-occupation', 'name': 'Say what you do', 'category': 'identity', 'cefr_rank': 2},
    {'slug': 'talk-about-family', 'name': 'Talk about your family', 'category': 'identity', 'cefr_rank': 2},
    
    # Social Interaction
    {'slug': 'greet-someone', 'name': 'Greet someone', 'category': 'social', 'cefr_rank': 1},
    {'slug': 'say-goodbye', 'name': 'Say goodbye', 'category': 'social', 'cefr_rank': 1},
    {'slug': 'thank-someone', 'name': 'Thank someone', 'category': 'social', 'cefr_rank': 1},
    {'slug': 'apologize', 'name': 'Apologize', 'category': 'social', 'cefr_rank': 1},
    
    # Needs & Requests
    {'slug': 'ask-for-something', 'name': 'Ask for something', 'category': 'needs', 'cefr_rank': 2},
    {'slug': 'order-food', 'name': 'Order food and drinks', 'category': 'needs', 'cefr_rank': 2},
    {'slug': 'ask-permission', 'name': 'Ask for permission', 'category': 'needs', 'cefr_rank': 2},
    {'slug': 'ask-for-help', 'name': 'Ask for help', 'category': 'needs', 'cefr_rank': 1},
    
    # Possession & Existence (CRÍTICOS)
    {'slug': 'express-possession', 'name': 'Say what you have', 'category': 'possession', 'cefr_rank': 2},
    {'slug': 'express-existence', 'name': 'Say what exists', 'category': 'possession', 'cefr_rank': 3},
    
    # Location & Direction
    {'slug': 'ask-where', 'name': 'Ask where something is', 'category': 'location', 'cefr_rank': 2},
    {'slug': 'describe-location', 'name': 'Describe where something is', 'category': 'location', 'cefr_rank': 3},
    
    # Shopping
    {'slug': 'ask-price', 'name': 'Ask about prices', 'category': 'shopping', 'cefr_rank': 2},
    {'slug': 'express-quantity', 'name': 'Say quantities', 'category': 'shopping', 'cefr_rank': 2},
    {'slug': 'choose-item', 'name': 'Choose items', 'category': 'shopping', 'cefr_rank': 1},
    
    # Time & Routine
    {'slug': 'tell-time', 'name': 'Tell the time', 'category': 'time', 'cefr_rank': 3},
    {'slug': 'talk-about-daily-routine', 'name': 'Talk about daily routine', 'category': 'time', 'cefr_rank': 3},
    
    # Ability & Preference
    {'slug': 'express-ability', 'name': 'Say what you can do', 'category': 'ability', 'cefr_rank': 2},
    {'slug': 'express-likes', 'name': 'Say what you like', 'category': 'ability', 'cefr_rank': 2},
    
    # Description
    {'slug': 'describe-people', 'name': 'Describe people', 'category': 'description', 'cefr_rank': 3},
    {'slug': 'describe-objects', 'name': 'Describe objects', 'category': 'description', 'cefr_rank': 2},
    
    # Communication Survival (CRÍTICOS)
    {'slug': 'ask-for-clarification', 'name': 'Ask for clarification', 'category': 'survival', 'cefr_rank': 1},
    {'slug': 'make-simple-statement-now', 'name': 'Say what you\'re doing now', 'category': 'survival', 'cefr_rank': 3},
    {'slug': 'express-simple-opinion', 'name': 'Give simple opinions', 'category': 'survival', 'cefr_rank': 3},
]

# ============================================
# CREAR O ACTUALIZAR INTENTS
# ============================================

created = 0
updated = 0

for idx, intent_data in enumerate(INTENTS_A1, 1):
    intent, was_created = CommunicativeIntent.objects.update_or_create(
        slug=intent_data['slug'],
        defaults={
            'name': intent_data['name'],
            'description': f'CEFR A1: {intent_data["name"]}',
            'category': intent_data['category'],
            'level': 'A1',
            'cefr_rank': intent_data['cefr_rank'],
            'is_core': True,
        }
    )
    
    if was_created:
        created += 1
        print(f"  ✅ Created: [{intent.cefr_rank}] {intent.name}")
    else:
        updated += 1
        print(f"  🔄 Updated: [{intent.cefr_rank}] {intent.name}")

print(f"\n📊 Summary:")
print(f"  ✅ Created: {created}")
print(f"  🔄 Updated: {updated}")
print(f"  📚 Total A1 Intents: {CommunicativeIntent.objects.filter(level='A1').count()}")

print("\n✅ CEFR A1 Core Intents seeded!")
print("🎯 28 intents abstractos - listos para realizar en contextos")
