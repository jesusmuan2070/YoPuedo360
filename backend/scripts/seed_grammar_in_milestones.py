"""
Seed GrammarInMilestone - Conecta Grammar Units con Milestones
Este script conecta las estructuras gramaticales universales con contextos específicos.

Run with: python scripts/seed_grammar_in_milestones.py (from backend folder)
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
django.setup()

from apps.grammar.models import GrammarUnit, GrammarInMilestone
from apps.scenarios.models import Scenario, Milestone

print("🔗 Conectando Grammar Units con Milestones...")

# ============================================
# MAPEO: Grammar -> Milestone
# ============================================

GRAMMAR_MILESTONE_CONNECTIONS = [
    # ==========================================
    # SCENARIO: Restaurant
    # ==========================================
    {
        'milestone_slug': 'restaurant-ordering',  # Ajusta según tus slugs reales
        'grammar_connections': [
            {
                'grammar_slug': 'can-infinitive',
                'introduction_order': 1,  # ⭐ SE ENSEÑA PRIMERO
                'importance_weight': 5,  # Crítico
                'is_primary_focus': True,
                'context_example': 'Can I have a coffee? / Can I see the menu?',
                'suggested_vocabulary_words': ['coffee', 'water', 'menu', 'bill', 'table']
            },
            {
                'grammar_slug': 'like-love-hate-noun',
                'introduction_order': 2,
                'importance_weight': 4,
                'is_primary_focus': False,
                'context_example': 'I like pizza. / I love Italian food.',
                'suggested_vocabulary_words': ['pizza', 'pasta', 'salad', 'wine']
            },
            {
                'grammar_slug': 'plural-nouns',
                'introduction_order': 3,
                'importance_weight': 3,
                'is_primary_focus': False,
                'context_example': 'Two coffees, please. / Three pizzas.',
                'suggested_vocabulary_words': ['coffee', 'pizza', 'fork', 'knife']
            },
        ]
    },
    
    # ==========================================
    # SCENARIO: Airport
    # ==========================================
    {
        'milestone_slug': 'airport-checkin',  # Ajusta según tus slugs
        'grammar_connections': [
            {
                'grammar_slug': 'can-infinitive',
                'introduction_order': 1,
                'importance_weight': 5,
                'is_primary_focus': True,
                'context_example': 'Can I see your passport? / Can I have your ticket?',
                'suggested_vocabulary_words': ['passport', 'ticket', 'seat', 'luggage']
            },
            {
                'grammar_slug': 'demonstratives',
                'introduction_order': 2,
                'importance_weight': 4,
                'is_primary_focus': False,
                'context_example': 'This is my passport. / That is my bag.',
                'suggested_vocabulary_words': ['passport', 'bag', 'suitcase', 'boarding pass']
            },
            {
                'grammar_slug': 'possessive-adjectives',
                'introduction_order': 3,
                'importance_weight': 4,
                'is_primary_focus': False,
                'context_example': 'My passport is here. / Your seat is 12A.',
                'suggested_vocabulary_words': ['passport', 'seat', 'ticket', 'luggage']
            },
        ]
    },
    
    # ==========================================
    # SCENARIO: Hotel
    # ==========================================
    {
        'milestone_slug': 'hotel-checkin',
        'grammar_connections': [
            {
                'grammar_slug': 'can-infinitive',
                'introduction_order': 1,
                'importance_weight': 5,
                'is_primary_focus': True,
                'context_example': 'Can I check in? / Can I have a wake-up call?',
                'suggested_vocabulary_words': ['room', 'key', 'reservation', 'checkout']
            },
            {
                'grammar_slug': 'there-is-are',
                'introduction_order': 2,
                'importance_weight': 4,
                'is_primary_focus': False,
                'context_example': 'Is there WiFi? / Are there towels in the room?',
                'suggested_vocabulary_words': ['wifi', 'towel', 'shower', 'bed']
            },
        ]
    },
    
    # ==========================================
    # SCENARIO: Shopping
    # ==========================================
    {
        'milestone_slug': 'shopping-browsing',
        'grammar_connections': [
            {
                'grammar_slug': 'simple-adjectives',
                'introduction_order': 1,
                'importance_weight': 5,
                'is_primary_focus': True,
                'context_example': 'This is too big. / That is very expensive.',
                'suggested_vocabulary_words': ['big', 'small', 'expensive', 'cheap', 'nice']
            },
            {
                'grammar_slug': 'demonstratives',
                'introduction_order': 2,
                'importance_weight': 5,
                'is_primary_focus': True,
                'context_example': 'How much is this? / Can I try those?',
                'suggested_vocabulary_words': ['shirt', 'shoes', 'dress', 'pants']
            },
        ]
    },
]

# ============================================
# CREAR CONEXIONES
# ============================================

created_count = 0
updated_count = 0
error_count = 0

for milestone_data in GRAMMAR_MILESTONE_CONNECTIONS:
    milestone_slug = milestone_data['milestone_slug']
    
    try:
        # Buscar el milestone (ajusta query según tu estructura)
        milestone = Milestone.objects.filter(slug=milestone_slug).first()
        
        if not milestone:
            print(f"  ⚠️  Milestone '{milestone_slug}' no encontrado - SKIP")
            error_count += 1
            continue
        
        print(f"\n🎯 Milestone: {milestone.name}")
        
        for grammar_conn in milestone_data['grammar_connections']:
            grammar_slug = grammar_conn['grammar_slug']
            
            try:
                # Buscar grammar unit (inglés)
                grammar = GrammarUnit.objects.get(
                    slug=grammar_slug,
                    target_language='en'
                )
                
                # Crear o actualizar conexión
                connection, created = GrammarInMilestone.objects.update_or_create(
                    grammar=grammar,
                    milestone=milestone,
                    defaults={
                        'introduction_order': grammar_conn['introduction_order'],
                        'importance_weight': grammar_conn['importance_weight'],
                        'is_primary_focus': grammar_conn['is_primary_focus'],
                        'context_example': grammar_conn['context_example'],
                        'suggested_vocabulary_words': grammar_conn.get('suggested_vocabulary_words', []),
                    }
                )
                
                if created:
                    created_count += 1
                    print(f"  ✅ Conectado: {grammar.name} (order: {grammar_conn['introduction_order']})")
                else:
                    updated_count += 1
                    print(f"  🔄 Actualizado: {grammar.name} (order: {grammar_conn['introduction_order']})")
                    
            except GrammarUnit.DoesNotExist:
                print(f"  ❌ Grammar '{grammar_slug}' no encontrado")
                error_count += 1
                
    except Exception as e:
        print(f"  ❌ Error procesando milestone '{milestone_slug}': {e}")
        error_count += 1

print(f"\n📊 Summary:")
print(f"  ✅ Creados: {created_count}")
print(f"  🔄 Actualizados: {updated_count}")
print(f"  ❌ Errores: {error_count}")
print(f"  📚 Total Conexiones: {GrammarInMilestone.objects.count()}")
print("\n✅ Conexiones Grammar-Milestone completadas!")
