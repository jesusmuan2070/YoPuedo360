"""
Seed Intent-Grammar Dependencies
Maps which grammar units each communicative intent requires
Run with: python scripts/seed_intent_grammar_dependencies.py
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
django.setup()

from apps.intents.models import CommunicativeIntent, IntentGrammarDependency
from apps.grammar.models import GrammarUnit

print("🔗 Seeding Intent-Grammar Dependencies...")

# Helper to get or skip
def get_intent(slug):
    try:
        return CommunicativeIntent.objects.get(slug=slug)
    except CommunicativeIntent.DoesNotExist:
        return None

def get_grammar(slug):
    try:
        return GrammarUnit.objects.get(slug=slug)
    except GrammarUnit.DoesNotExist:
        return None

# ============================================
# A1 INTENT → GRAMMAR MAPPINGS
# ============================================

A1_MAPPINGS = [
    # Greetings & Basic Interaction
    ('greet-someone', 'verb-to-be', True, 1, "Need 'I am...' for introductions"),
    ('introduce-self', 'verb-to-be', True, 1, "Core for 'My name is...'"),
    ('introduce-self', 'possessive-adjectives', True, 2, "For 'my name', 'my job'"),
    
    # Ordering & Requests
    ('order-food', 'can-infinitive', True, 1, "Can I have... / Can I get..."),
    ('order-food', 'a-an-articles', True, 2, "a coffee, an apple"),
    ('order-food', 'countable-uncountable', False, 3, "some water vs two coffees"),
    ('ask-for-something', 'can-infinitive', True, 1, "Can I have...?"),
    ('ask-permission', 'can-infinitive', True, 1, "Can I...?"),
    
    # Shopping & Prices
    ('ask-price', 'how-much', True, 1, "How much is...?"),
    ('ask-price', 'demonstratives', True, 2, "this / that item"),
    ('choose-item', 'demonstratives', True, 1, "I want this one"),
    ('choose-item', 'determiners', False, 2, "this, that, these, those"),
    
    # Location
    ('ask-where', 'question-words', True, 1, "Where is...?"),
    ('ask-where', 'prepositions-place', True, 2, "in, on, at, next to"),
    ('describe-location', 'prepositions-place', True, 1, "It's next to..."),
    ('describe-location', 'verb-to-be', True, 2, "The bank is..."),
    
    # Possession
    ('express-possession', 'possessive-adjectives', True, 1, "my bag, his car"),
    ('express-possession', 'have-has', True, 2, "I have a phone"),
    
    # Existence
    ('express-existence', 'there-is-are', True, 1, "There is a problem"),
    
    # Description
    ('describe-people', 'verb-to-be', True, 1, "She is tall"),
    ('describe-people', 'adjectives-basic', True, 2, "tall, short, young"),
    ('describe-objects', 'verb-to-be', True, 1, "It is big"),
    ('describe-objects', 'adjectives-basic', True, 2, "color, size adjectives"),
    
    # Likes & Preferences
    ('express-likes', 'present-simple', True, 1, "I like / love"),
    ('express-likes', 'object-pronouns', False, 2, "I like it"),
    
    # Ability
    ('express-ability', 'can-infinitive', True, 1, "I can swim"),
    
    # Time & Routine
    ('tell-time', 'numbers', True, 1, "at 3 o'clock"),
    ('tell-time', 'prepositions-time', True, 2, "at, on, in"),
    ('talk-about-daily-routine', 'present-simple', True, 1, "I wake up at..."),
    ('talk-about-daily-routine', 'prepositions-time', True, 2, "in the morning"),
    
    # Statements
    ('make-simple-statement-now', 'present-continuous', True, 1, "I am working"),
    ('express-simple-opinion', 'present-simple', True, 1, "I think..."),
]

# ============================================
# A2 INTENT → GRAMMAR MAPPINGS  
# ============================================

A2_MAPPINGS = [
    # Past Experience
    ('talk-about-past-experience', 'past-simple', True, 1, "I visited Paris"),
    ('talk-about-past-experience', 'prepositions-time', True, 2, "in 2020, last year"),
    ('talk-about-past-habit', 'used-to', True, 1, "I used to smoke"),
    ('talk-about-past-events', 'past-simple', True, 1, "It happened yesterday"),
    
    # Future & Plans
    ('talk-about-plans', 'going-to-future', True, 1, "I'm going to travel"),
    ('talk-about-future-intentions', 'going-to-future', True, 1, "We're going to visit"),
    
    # Comparisons
    ('compare-items', 'comparatives', True, 1, "This is cheaper than that"),
    ('compare-items', 'superlatives', False, 2, "This is the cheapest"),
    
    # Complaints & Problems
    ('make-simple-complaint', 'present-simple', True, 1, "This doesn't work"),
    ('make-simple-complaint', 'too-enough', True, 2, "It's too expensive"),
    ('report-a-problem', 'present-perfect-introduction', False, 1, "The heater has broken"),
    ('ask-for-solution', 'can-infinitive', True, 1, "Can you fix it?"),
    
    # Obligations & Advice
    ('express-obligation', 'have-to-must', True, 1, "I have to work"),
    ('give-advice-simple', 'should-ought-to', True, 1, "You should rest"),
    
    # Social Interaction
    ('make-invitation', 'would-you-like', True, 1, "Would you like to come?"),
    ('make-invitation', 'going-to-future', False, 2, "We're going to..."),
    ('suggest-activity', 'should-ought-to', True, 1, "We should go"),
    ('arrange-meeting', 'going-to-future', True, 1, "Let's meet at..."),
    ('arrange-meeting', 'prepositions-time', True, 2, "at 5pm, on Monday"),
    
    # Directions
    ('give-simple-directions', 'imperatives', True, 1, "Turn left, go straight"),
    ('give-simple-directions', 'prepositions-place', True, 2, "next to, opposite"),
    
    # Preferences & Opinion
    ('express-preference', 'would-rather', True, 1, "I prefer / I'd rather"),
    ('express-preference', 'comparatives', False, 2, "I like this more than that"),
    ('express-dislikes', 'present-simple', True, 1, "I don't like..."),
    ('ask-for-opinion', 'question-words', True, 1, "What do you think?"),
    
    # Health & Feelings
    ('express-feelings-basic', 'verb-to-be', True, 1, "I am happy/sad"),
    ('express-feelings-basic', 'adverbs-manner', False, 2, "I feel badly"),
    ('describe-symptoms', 'present-simple', True, 1, "My head hurts"),
    ('describe-symptoms', 'have-has', True, 2, "I have a headache"),
    ('express-physical-state', 'verb-to-be', True, 1, "I am cold/hot"),
    
    # Quantity & Frequency
    ('express-amount', 'countable-uncountable', True, 1, "How much/many"),
    ('express-amount', 'some-any', True, 2, "some milk, any questions"),
    ('express-frequency', 'adverbs-frequency', True, 1, "always, sometimes, never"),
    
    # Communication
    ('ask-someone-to-repeat', 'question-tags', False, 1, "Sorry, what?"),
    ('check-understanding', 'question-tags', True, 1, "You mean..., right?"),
    
    # Offers
    ('make-offer', 'would-you-like', True, 1, "Would you like...?"),
    ('accept-offer', 'present-simple', True, 1, "Yes, please"),
    ('refuse-offer', 'present-simple', True, 1, "No, thank you"),
]

# ============================================
# SAVE TO DATABASE
# ============================================

created = 0
skipped = 0

all_mappings = A1_MAPPINGS + A2_MAPPINGS

for intent_slug, grammar_slug, is_critical, order, usage_note in all_mappings:
    intent = get_intent(intent_slug)
    grammar = get_grammar(grammar_slug)
    
    if not intent:
        print(f"  ⚠️  Intent not found: {intent_slug}")
        skipped += 1
        continue
    
    if not grammar:
        print(f"  ⚠️  Grammar not found: {grammar_slug}")
        skipped += 1
        continue
    
    obj, created_flag = IntentGrammarDependency.objects.get_or_create(
        intent=intent,
        grammar=grammar,
        defaults={
            'is_critical': is_critical,
            'order': order,
            'usage_note': usage_note
        }
    )
    
    if created_flag:
        created += 1
        critical = "CRITICAL" if is_critical else "optional"
        print(f"  ✅ {intent.slug} → {grammar.slug} ({critical})")

print(f"\n✅ Seeding complete!")
print(f"   Created: {created}")
print(f"   Skipped: {skipped}")
print(f"   Total dependencies: {IntentGrammarDependency.objects.count()}")
