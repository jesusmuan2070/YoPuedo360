"""
Seed A2 Communicative Intents
Based on CEFR A2 descriptors - intermediate elementary level
Run with: python scripts/seed_intents_a2.py
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
django.setup()

from apps.intents.models import CommunicativeIntent

print("🎯 Seeding A2 Communicative Intents...")

# ============================================
# A2 INTENTS (42 total)
# ============================================

A2_INTENTS = [
    # ========================================
    # IDENTITY & EXPERIENCE (Past added)
    # ========================================
    
    {
        'slug': 'talk-about-past-experience',
        'name': 'Talk about past experiences',
        'category': 'identity',
        'level': 'A2',
        'cefr_rank': 1,
        'is_core': True,
        'description': 'Describe things you did or experienced in the past',
    },
    
    {
        'slug': 'talk-about-past-habit',
        'name': 'Talk about past habits',
        'category': 'identity',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Describe things you used to do (used to)',
    },
    
    # ========================================
    # TIME & EVENTS (Key A2 skill)
    # ========================================
    
    {
        'slug': 'talk-about-past-events',
        'name': 'Talk about past events',
        'category': 'time',
        'level': 'A2',
        'cefr_rank': 1,
        'is_core': True,
        'description': 'Describe what happened in the past',
    },
    
    {
        'slug': 'talk-about-dates',
        'name': 'Talk about dates and schedules',
        'category': 'time',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Discuss specific dates and times',
    },
    
    {
        'slug': 'talk-about-plans',
        'name': 'Talk about plans',
        'category': 'time',
        'level': 'A2',
        'cefr_rank': 1,
        'is_core': True,
        'description': 'Describe future plans (going to)',
    },
    
    {
        'slug': 'talk-about-future-intentions',
        'name': 'Express future intentions',
        'category': 'time',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Talk about what you intend to do',
    },
    
    # ========================================
    # DAILY LIFE (More detail than A1)
    # ========================================
    
    {
        'slug': 'talk-about-free-time',
        'name': 'Talk about free time activities',
        'category': 'daily_life',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Describe what you do in your free time',
    },
    
    {
        'slug': 'talk-about-hobbies',
        'name': 'Talk about hobbies and interests',
        'category': 'daily_life',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Discuss your hobbies and what you enjoy doing',
    },
    
    {
        'slug': 'describe-places',
        'name': 'Describe places',
        'category': 'description',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Describe cities, buildings, rooms, etc.',
    },
    
    # ========================================
    # NEEDS & PROBLEMS (A2 adds complaints)
    # ========================================
    
    {
        'slug': 'make-simple-complaint',
        'name': 'Make a simple complaint',
        'category': 'needs',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Express dissatisfaction politely',
    },
    
    {
        'slug': 'report-a-problem',
        'name': 'Report a problem',
        'category': 'needs',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Explain that something is wrong',
    },
    
    {
        'slug': 'ask-for-solution',
        'name': 'Ask for a solution',
        'category': 'needs',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Request help to fix a problem',
    },
    
    # ========================================
    # SHOPPING & TRANSACTIONS (More complex)
    # ========================================
    
    {
        'slug': 'compare-items',
        'name': 'Compare items',
        'category': 'shopping',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Compare two or more products (comparatives)',
    },
    
    {
        'slug': 'ask-for-bill',
        'name': 'Ask for the bill',
        'category': 'transactional',
        'level': 'A2',
        'cefr_rank': 3,
        'is_core': False,
        'description': 'Request the check in a restaurant',
    },
    
    {
        'slug': 'pay-for-service',
        'name': 'Pay for a service',
        'category': 'transactional',
        'level': 'A2',
        'cefr_rank': 3,
        'is_core': False,
        'description': 'Complete a payment transaction',
    },
    
    # ========================================
    # OPINION & PREFERENCE (Simple level)
    # ========================================
    
    {
        'slug': 'express-dislikes',
        'name': 'Express dislikes',
        'category': 'opinion',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Say what you don\'t like',
    },
    
    {
        'slug': 'express-obligation',
        'name': 'Express obligation',
        'category': 'modal',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Say what you must/have to do',
    },
    
    {
        'slug': 'give-advice-simple',
        'name': 'Give simple advice',
        'category': 'social',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Suggest what someone should do',
    },
    
    {
        'slug': 'express-preference',
        'name': 'Express preference',
        'category': 'opinion',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Say what you prefer between options',
    },
    
    # ========================================
    # LOCATION & DIRECTIONS (Beyond A1)
    # ========================================
    
    {
        'slug': 'give-simple-directions',
        'name': 'Give simple directions',
        'category': 'location',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Tell someone how to get somewhere',
    },
    
    # ========================================
    # SOCIAL INTERACTION (Important A2)
    # ========================================
    
    {
        'slug': 'make-invitation',
        'name': 'Make an invitation',
        'category': 'social',
        'level': 'A2',
        'cefr_rank': 1,
        'is_core': True,
        'description': 'Invite someone to do something',
    },
    
    {
        'slug': 'accept-invitation',
        'name': 'Accept an invitation',
        'category': 'social',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Say yes to an invitation',
    },
    
    {
        'slug': 'decline-invitation',
        'name': 'Decline an invitation',
        'category': 'social',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Say no to an invitation politely',
    },
    
    {
        'slug': 'suggest-activity',
        'name': 'Suggest an activity',
        'category': 'social',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Propose something to do together',
    },
    
    {
        'slug': 'arrange-meeting',
        'name': 'Arrange a meeting',
        'category': 'social',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Set up a time and place to meet',
    },
    
    # ========================================
    # COMMUNICATION & INTERACTION
    # ========================================
    
    {
        'slug': 'ask-someone-to-repeat',
        'name': 'Ask someone to repeat',
        'category': 'survival',
        'level': 'A2',
        'cefr_rank': 1,
        'is_core': True,
        'description': 'Request someone to say something again',
    },
    
    {
        'slug': 'check-understanding',
        'name': 'Check understanding',
        'category': 'survival',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Verify that you understood correctly',
    },
    
    {
        'slug': 'correct-mistake',
        'name': 'Correct a mistake',
        'category': 'social',
        'level': 'A2',
        'cefr_rank': 3,
        'is_core': False,
        'description': 'Politely correct information',
    },
    
    # ========================================
    # FEELINGS & STATES (Simple A2)
    # ========================================
    
    {
        'slug': 'express-feelings-basic',
        'name': 'Express basic feelings',
        'category': 'emotion',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Say how you feel (happy, sad, tired, etc.)',
    },
    
    {
        'slug': 'express-physical-state',
        'name': 'Express physical state',
        'category': 'health',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Describe physical sensations (hot, cold, hungry)',
    },
    
    {
        'slug': 'describe-symptoms',
        'name': 'Describe health symptoms',
        'category': 'health',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Explain what hurts or feels wrong',
    },
    
    # ========================================
    # INFORMATION & DESCRIPTION
    # ========================================
    
    {
        'slug': 'ask-for-information',
        'name': 'Ask for specific information',
        'category': 'information',
        'level': 'A2',
        'cefr_rank': 1,
        'is_core': True,
        'description': 'Request detailed information about something',
    },
    
    {
        'slug': 'give-information',
        'name': 'Give information',
        'category': 'information',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Provide details and facts',
    },
    
    {
        'slug': 'describe-weather',
        'name': 'Describe weather',
        'category': 'description',
        'level': 'A2',
        'cefr_rank': 3,
        'is_core': False,
        'description': 'Talk about weather conditions',
    },
    
    # ========================================
    # QUANTITY & MEASUREMENT
    # ========================================
    
    {
        'slug': 'express-amount',
        'name': 'Express amount',
        'category': 'quantity',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Say how much or how many (much/many)',
    },
    
    {
        'slug': 'express-frequency',
        'name': 'Express frequency',
        'category': 'time',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Say how often something happens',
    },
    
    # ========================================
    # ASKING & OFFERING
    # ========================================
    
    {
        'slug': 'make-offer',
        'name': 'Make an offer',
        'category': 'social',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Offer to do something for someone',
    },
    
    {
        'slug': 'accept-offer',
        'name': 'Accept an offer',
        'category': 'social',
        'level': 'A2',
        'cefr_rank': 3,
        'is_core': False,
        'description': 'Say yes to someone\'s offer',
    },
    
    {
        'slug': 'refuse-offer',
        'name': 'Refuse an offer',
        'category': 'social',
        'level': 'A2',
        'cefr_rank': 3,
        'is_core': False,
        'description': 'Say no to someone\'s offer politely',
    },
    
    # ========================================
    # ADDITIONAL A2 INTENTS
    # ========================================
    
    {
        'slug': 'express-surprise',
        'name': 'Express surprise',
        'category': 'emotion',
        'level': 'A2',
        'cefr_rank': 3,
        'is_core': False,
        'description': 'React to unexpected information',
    },
    
    {
        'slug': 'ask-for-opinion',
        'name': 'Ask for someone\'s opinion',
        'category': 'social',
        'level': 'A2',
        'cefr_rank': 2,
        'is_core': True,
        'description': 'Request someone\'s view on something',
    },
]

# ============================================
# SAVE TO DATABASE
# ============================================

created = 0
updated = 0

for intent_data in A2_INTENTS:
    obj, created_flag = CommunicativeIntent.objects.update_or_create(
        slug=intent_data['slug'],
        defaults=intent_data
    )
    
    if created_flag:
        created += 1
        print(f"  ✅ Created: {intent_data['name']}")
    else:
        updated += 1
        print(f"  🔄 Updated: {intent_data['name']}")

print(f"\n✅ Seeding complete!")
print(f"   Created: {created}")
print(f"   Updated: {updated}")
print(f"   Total A2 Intents: {CommunicativeIntent.objects.filter(level='A2').count()}")
print(f"\n📊 Breakdown:")
print(f"   Core intents: {CommunicativeIntent.objects.filter(level='A2', is_core=True).count()}")
print(f"   Supplementary: {CommunicativeIntent.objects.filter(level='A2', is_core=False).count()}")
