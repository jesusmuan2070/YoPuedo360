"""
AI-Powered Intent Realization Population
Conecta Intents con Milestones usando AI para generar ejemplos contextuales.

Similar a ai_populate_grammar_examples.py pero para IntentRealization.

Run with: python scripts/ai_populate_intent_realizations.py
"""

import os
import sys
import django
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
django.setup()

from apps.intents.models import CommunicativeIntent, IntentRealization
from apps.scenarios.models import Milestone
from apps.ai_services.clients.openai_client import OpenAIClient


print("🤖 Poblando IntentRealization con ejemplos contextuales IA...\n")

# ============================================
# CONFIGURACIÓN
# ============================================

DRY_RUN = True  # Cambiar a False para guardar
LIMIT_MILESTONES = 1  # None = todos, número para testing
MODEL = "gpt-4o-mini"

# ============================================
# MAPEO INTENT → SCENARIOS
# ============================================

INTENT_SCENARIO_MAP = {
    # Identity intents → varios scenarios
    'introduce-self': ['greetings', 'airport', 'hotel', 'work'],
    'talk-about-origin': ['greetings', 'airport', 'travel'],
    'describe-occupation': ['greetings', 'work', 'networking'],
    'talk-about-family': ['greetings', 'social'],
    
    # Social intents → universal
    'greet-someone': ['greetings', 'restaurant', 'shopping', 'hotel', 'work'],
    'say-goodbye': ['greetings', 'restaurant', 'shopping', 'hotel', 'work'],
    'thank-someone': ['restaurant', 'shopping', 'hotel', 'service'],
    'apologize': ['restaurant', 'shopping', 'hotel', 'service'],
    
    # Needs intents
    'ask-for-something': ['restaurant', 'shopping', 'hotel', 'airport'],
    'order-food': ['restaurant', 'cafe', 'airplane'],
    'ask-permission': ['restaurant', 'hotel', 'work', 'social'],
    'ask-for-help': ['shopping', 'airport', 'hotel', 'street'],
    
    # Possession
    'express-possession': ['shopping', 'airport', 'hotel', 'customs'],
    'express-existence': ['shopping', 'hotel', 'city', 'directions'],
    
    # Location
    'ask-where': ['shopping', 'airport', 'hotel', 'city', 'street'],
    'describe-location': ['directions', 'city', 'hotel'],
    
    # Shopping
    'ask-price': ['shopping', 'restaurant', 'market', 'taxi'],
    'express-quantity': ['shopping', 'restaurant', 'market'],
    'choose-item': ['shopping', 'restaurant', 'market'],
    
    # Time
    'tell-time': ['work', 'appointments', 'travel'],
    'talk-about-daily-routine': ['work', 'social', 'health'],
    
    # Ability
    'express-ability': ['work', 'social', 'sports', 'language'],
    'express-likes': ['restaurant', 'social', 'hobbies'],
    
    # Description
    'describe-people': ['social', 'work', 'police'],
    'describe-objects': ['shopping', 'lost-found', 'police'],
    
    # Survival
    'ask-for-clarification': ['all'],  # Universal
    'make-simple-statement-now': ['work', 'social', 'phone'],
    'express-simple-opinion': ['restaurant', 'shopping', 'social'],
}

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def intent_matches_milestone(intent, milestone):
    """
    Determina si un intent es relevante para un milestone.
    """
    scenario_slug = milestone.scenario.slug
    
    # Intents universales
    if intent.slug in INTENT_SCENARIO_MAP:
        scenarios = INTENT_SCENARIO_MAP[intent.slug]
        
        if 'all' in scenarios:
            return True
        
        # Match directo de slug
        if scenario_slug in scenarios:
            return True
        
        # Match parcial (ej: 'restaurant' matchea 'restaurant-fancy')
        for mapped_scenario in scenarios:
            if mapped_scenario in scenario_slug or scenario_slug in mapped_scenario:
                return True
    
    return False


def calculate_priority(intent, milestone):
    """
    Calcula prioridad del intent en este milestone.
    1 = crítico, 5 = opcional
    """
    # Intents de supervivencia siempre tienen alta prioridad
    if intent.category == 'survival':
        return 1
    
    # Social interactions en primeros milestones
    if intent.category == 'social' and milestone.order <= 2:
        return 1
    
    # Usar cefr_rank del intent como base
    return intent.cefr_rank


def generate_intent_examples(intent, milestone, client):
    """
    Usa AI para generar ejemplos contextuales del intent.
    """
    
    system_prompt = """Eres un experto profesor de idiomas CEFR especializado en crear ejemplos prácticos.

Tu tarea es generar 3-4 oraciones que un estudiante necesitaría para lograr una intención comunicativa específica en un contexto real.

Los ejemplos deben ser:
- Naturales y realistas
- Apropiados para el nivel CEFR
- Específicos del contexto/scenario
- Inmediatamente útiles

Responde SOLO con JSON válido."""

    user_prompt = f"""Contexto:
- Scenario: {milestone.scenario.name}
- Milestone: {milestone.name}
- Nivel: {milestone.level}

Intención comunicativa:
- Intent: {intent.name}
- Descripción: {intent.description}

Genera 3-4 oraciones específicas que el usuario necesita para "{intent.name}" en el contexto de "{milestone.scenario.name} - {milestone.name}".

Formato JSON:
{{
  "examples": ["Example 1.", "Example 2.", "Example 3."],
  "difficulty": 1-5,
  "estimated_time": 5-15 (minutos),
  "priority": 1-5,
  "reasoning": "brief explanation"
}}

difficulty: qué tan difícil es en ESTE contexto
priority: 1=crítico para este milestone, 5=opcional"""

    try:
        response = client.complete_json(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=300
        )
        
        return {
            'examples': response.get('examples', []),
            'difficulty': response.get('difficulty', 2),
            'estimated_time': response.get('estimated_time', 10),
            'priority': response.get('priority', 3),
            'reasoning': response.get('reasoning', '')
        }
        
    except Exception as e:
        print(f"      ❌ Error AI: {e}")
        return None


# ============================================
# PROCESO PRINCIPAL
# ============================================

client = OpenAIClient(model=MODEL)

# Obtener milestones
milestones_query = Milestone.objects.all().select_related('scenario')
if LIMIT_MILESTONES:
    milestones_query = milestones_query[:LIMIT_MILESTONES]

total_milestones = milestones_query.count()
print(f"📊 Total milestones a procesar: {total_milestones}")
print(f"🔧 Modo: {'DRY RUN (no guarda)' if DRY_RUN else 'PRODUCTION (guarda en DB)'}")
print(f"🤖 Modelo: {MODEL}\n")

total_created = 0
total_skipped = 0
total_errors = 0
cost_estimate = Decimal('0')

for idx, milestone in enumerate(milestones_query, 1):
    print(f"\n[{idx}/{total_milestones}] 📍 {milestone.scenario.name} - {milestone.name} ({milestone.level})")
    
    # Obtener todos los intents del nivel
    all_intents = CommunicativeIntent.objects.filter(
        level=milestone.level,
        is_core=True
    ).order_by('cefr_rank')
    
    # Filtrar intents relevantes para este milestone
    relevant_intents = [
        intent for intent in all_intents 
        if intent_matches_milestone(intent, milestone)
    ]
    
    print(f"   Intents relevantes: {len(relevant_intents)}/{all_intents.count()}")
    
    milestone_created = 0
    
    for intent in relevant_intents:
        # Verificar si ya existe
        existing = IntentRealization.objects.filter(
            intent=intent,
            milestone=milestone
        ).exists()
        
        if existing:
            total_skipped += 1
            continue
        
        # Generar ejemplos con AI
        print(f"   🤖 Generando: {intent.name}...", end=' ')
        
        ai_result = generate_intent_examples(intent, milestone, client)
        
        if not ai_result or not ai_result['examples']:
            print("❌ No examples")
            total_errors += 1
            continue
        
        # Estimar costo
        cost_estimate += Decimal('0.001')
        
        if not DRY_RUN:
            # Crear registro
            IntentRealization.objects.create(
                intent=intent,
                milestone=milestone,
                example_chunks=ai_result['examples'],
                difficulty=ai_result['difficulty'],
                estimated_time=ai_result['estimated_time'],
                priority=calculate_priority(intent, milestone),
                is_primary=(ai_result['priority'] == 1)
            )
        
        print(f"✅ (priority: {ai_result['priority']}, difficulty: {ai_result['difficulty']})")
        total_created += 1
        milestone_created += 1
    
    print(f"   → {milestone_created} realizaciones {'generadas' if not DRY_RUN else 'procesadas'}")


# ============================================
# RESUMEN FINAL
# ============================================

print("\n" + "="*60)
print("📊 RESUMEN FINAL")
print("="*60)
print(f"✅ Realizaciones creadas: {total_created}")
print(f"⏭️  Ya existían: {total_skipped}")
print(f"❌ Errores: {total_errors}")
print(f"💰 Costo estimado: ${cost_estimate:.2f} USD")
print(f"📚 Total en DB: {IntentRealization.objects.count()}")

if DRY_RUN:
    print("\n⚠️  DRY RUN - Ningún registro fue guardado en la DB")
    print("   Cambia DRY_RUN = False para guardar")

print("\n✅ Proceso completado!")
