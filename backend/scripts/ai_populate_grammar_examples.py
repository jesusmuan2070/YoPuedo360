"""
AI-Powered Grammar Examples Population
Genera automáticamente ejemplos contextuales para cada milestone usando OpenAI.

Run with: python scripts/ai_populate_grammar_examples.py
"""

import os
import sys
import django
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
django.setup()

from apps.grammar.models import GrammarUnit, GrammarInMilestone
from apps.scenarios.models import Milestone
from apps.ai_services.clients.openai_client import OpenAIClient


print("🤖 Poblando GrammarInMilestone con ejemplos generados por AI...\n")

# ============================================
# CONFIGURACIÓN
# ============================================

DRY_RUN = False  # Cambiar a True para solo ver qué haría sin crear registros
LIMIT_MILESTONES = 1  # None = todos, o número para testing (ej: 10)
MODEL = "gpt-4o-mini"  # Modelo a usar

# ============================================
# NIVEL HIERARCHY (para determinar grammar relevantes)
# ============================================

LEVEL_HIERARCHY = {
    'A1': ['A1'],
    'A2': ['A1', 'A2'],
    'B1': ['A1', 'A2', 'B1'],
    'B2': ['A1', 'A2', 'B1', 'B2'],
    'C1': ['A1', 'A2', 'B1', 'B2', 'C1'],
    'C2': ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'],
}

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def get_milestone_level(milestone):
    """
    Extrae el nivel CEFR del milestone.
    """
    # El milestone tiene campo 'level' según seed_all_scenarios.py
    if hasattr(milestone, 'level'):
        return milestone.level
    
    # Fallback: extraer del nombre o usar default
    name_upper = milestone.name.upper()
    for level in ['C2', 'C1', 'B2', 'B1', 'A2', 'A1']:
        if level in name_upper:
            return level
    
    # Default conservador
    return 'A1'


def get_relevant_grammar(milestone_level, target_language='en'):
    """
    Obtiene grammar units relevantes para este milestone.
    """
    valid_levels = LEVEL_HIERARCHY.get(milestone_level, ['A1'])
    
    return GrammarUnit.objects.filter(
        target_language=target_language,
        level__in=valid_levels
    ).order_by('pedagogical_sequence')


def generate_context_examples(grammar, milestone, client):
    """
    Usa AI para generar ejemplos contextuales.
    """
    
    system_prompt = """Eres un experto profesor de idiomas especializado en crear ejemplos prácticos.
Tu tarea es generar 3-4 oraciones de ejemplo que usen una estructura gramatical específica
en un contexto real de comunicación.

Los ejemplos deben ser:
- Naturales y realistas
- Apropiados para el nivel CEFR indicado
- Relevantes al contexto específico
- Claros y directos

Responde SOLO con JSON válido."""

    user_prompt = f"""Contexto:
- Scenario: {milestone.scenario.name}
- Milestone: {milestone.name}
- Nivel: {get_milestone_level(milestone)}

Estructura gramatical:
- Name: {grammar.name}
- Form: {grammar.form}
- Meaning: {grammar.meaning_en}

Genera 3-4 oraciones de ejemplo usando "{grammar.name}" en el contexto de "{milestone.scenario.name} - {milestone.name}".

Formato JSON:
{{
  "examples": ["Example 1", "Example 2", "Example 3", "Example 4"],
  "importance": 1-5,
  "reasoning": "brief explanation why this grammar is relevant here"
}}

importance scale:
1 = opcional
2 = útil
3 = importante
4 = muy importante
5 = crítico para este contexto"""

    try:
        response = client.complete_json(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=300
        )
        
        return {
            'examples': response.get('examples', ''),
            'importance': response.get('importance', 3),
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
    milestone_level = get_milestone_level(milestone)
    
    print(f"\n[{idx}/{total_milestones}] 📍 {milestone.scenario.name} - {milestone.name} ({milestone_level})")
    
    # Obtener grammar relevantes
    relevant_grammar = get_relevant_grammar(milestone_level, target_language='en')
    grammar_count = relevant_grammar.count()
    
    print(f"   Grammar relevantes: {grammar_count}")
    
    milestone_created = 0
    
    for grammar in relevant_grammar:
        # Verificar si ya existe
        existing = GrammarInMilestone.objects.filter(
            grammar=grammar,
            milestone=milestone
        ).exists()
        
        if existing:
            total_skipped += 1
            continue
        
        # Generar ejemplos con AI
        print(f"   🤖 Generando: {grammar.name}...", end=' ')
        
        ai_result = generate_context_examples(grammar, milestone, client)
        
        if not ai_result or not ai_result['examples']:
            print("❌ No examples")
            total_errors += 1
            continue
        
        # Estimar costo (aproximado)
        cost_estimate += Decimal('0.001')  # ~$0.001 por request
        
        if not DRY_RUN:
            # Crear registro
            GrammarInMilestone.objects.create(
                grammar=grammar,
                milestone=milestone,
                context_example=ai_result['examples'],
                importance_weight=ai_result['importance'],
                introduction_order=grammar.pedagogical_sequence,
                is_primary_focus=(ai_result['importance'] == 5)
            )
        
        print(f"✅ (importance: {ai_result['importance']})")
        total_created += 1
        milestone_created += 1
    
    print(f"   → {milestone_created} ejemplos {'generados' if not DRY_RUN else 'procesados'}")


# ============================================
# RESUMEN FINAL
# ============================================

print("\n" + "="*60)
print("📊 RESUMEN FINAL")
print("="*60)
print(f"✅ Ejemplos creados: {total_created}")
print(f"⏭️  Ya existían: {total_skipped}")
print(f"❌ Errores: {total_errors}")
print(f"💰 Costo estimado: ${cost_estimate:.2f} USD")
print(f"📚 Total en DB: {GrammarInMilestone.objects.count()}")

if DRY_RUN:
    print("\n⚠️  DRY RUN - Ningún registro fue guardado en la DB")
    print("   Cambia DRY_RUN = False para guardar")

print("\n✅ Proceso completado!")
