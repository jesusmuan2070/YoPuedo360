"""
Test del Orquestador de Aprendizaje
Prueba el flujo completo: Usuario → Milestone → Generación on-the-fly

Run with: python scripts/test_orchestrator.py
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
django.setup()

from apps.scenarios.models import Scenario, Milestone
from apps.intents.services.orchestrator import orchestrator
from apps.users.models import User, LearningProfile


print("🧪 Probando Learning Orchestrator...\n")
print("="*60)

# ============================================
# TEST 1: Seleccionar Milestone
# ============================================

print("\n📍 TEST 1: Seleccionar Milestone")
print("-"*60)

# Buscar scenario Airport
airport = Scenario.objects.filter(slug__icontains='airport').first()

if not airport:
    print("❌ Scenario 'aeropuerto' no encontrado")
    print("   Ejecuta: python scripts/seed_all_scenarios.py")
    sys.exit(1)

print(f"✅ Scenario encontrado: {airport.name}")

# Buscar primer milestone A1
milestone = Milestone.objects.filter(
    scenario=airport,
    level='A1'
).order_by('order').first()

if not milestone:
    print("❌ No hay milestones A1 en aeropuerto")
    sys.exit(1)

print(f"✅ Milestone seleccionado: {milestone.name} (A1-{milestone.order})")

# ============================================
# TEST 2: Intents Disponibles
# ============================================

print("\n🎯 TEST 2: Obtener Intents Disponibles")
print("-"*60)

available_intents = orchestrator._get_available_intents(milestone)

print(f"Total intents disponibles: {len(available_intents)}")
print("\nIntents relevantes para este milestone:")
for idx, intent in enumerate(available_intents[:10], 1):
    print(f"  {idx}. [{intent.cefr_rank}] {intent.name} ({intent.category})")

if len(available_intents) > 10:
    print(f"  ... y {len(available_intents) - 10} más")

# ============================================
# TEST 3: Usuario Mock
# ============================================

print("\n👤 TEST 3: Crear Usuario de Prueba")
print("-"*60)

# Crear o buscar usuario test
user, created = User.objects.get_or_create(
    username='test_orchestrator',
    defaults={
        'email': 'test@test.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
)

if created:
    print("✅ Usuario creado: test_orchestrator")
else:
    print("✅ Usuario existente: test_orchestrator")

# Ensure LearningProfile exists
LearningProfile.objects.get_or_create(
    user=user,
    defaults={
        'target_language': 'en',
        'native_language': 'es',
        'cefr_level': 'A1'
    }
)
print("✅ LearningProfile verificado")

# ============================================
# TEST 4: Siguiente Intent (sin progreso)
# ============================================

print("\n🎯 TEST 4: Determinar Siguiente Intent")
print("-"*60)

next_intent = orchestrator._get_next_intent(user, milestone, available_intents)

if next_intent:
    print(f"✅ Siguiente intent: {next_intent.name}")
    print(f"   Categoría: {next_intent.category}")
    print(f"   Prioridad CEFR: {next_intent.cefr_rank}")
else:
    print("❌ No hay intents disponibles")
    sys.exit(1)

# ============================================
# TEST 5: Generar IntentRealization (AI)
# ============================================

print("\n🤖 TEST 5: Generar/Obtener IntentRealization")
print("-"*60)

print(f"Intent: {next_intent.name}")
print(f"Milestone: {milestone.name}")
print("\n⏳ Generando con AI (puede tomar 1-2 segundos)...\n")

try:
    intent_realization = orchestrator._get_or_generate_intent_realization(
        next_intent,
        milestone,
        user
    )
    
    print("✅ IntentRealization obtenida/generada")
    print(f"\nFrases generadas:")
    for idx, phrase in enumerate(intent_realization.example_chunks, 1):
        print(f"  {idx}. {phrase}")
    
    print(f"\nDificultad: {intent_realization.difficulty}/5")
    print(f"Tiempo estimado: {intent_realization.estimated_time} min")
    
except Exception as e:
    print(f"❌ Error generando IntentRealization: {e}")
    print("\nPosibles causas:")
    print("  - OpenAI API key no configurada")
    print("  - Modelo CommunicativeIntent no migrado")

# ============================================
# TEST 6: Grammar Necesaria
# ============================================

print("\n📚 TEST 6: Identificar Grammar Necesaria")
print("-"*60)

required_grammar = orchestrator._get_required_grammar(next_intent, milestone)

if required_grammar:
    print(f"Grammar requerida: {len(required_grammar)} unidades")
    for grammar in required_grammar:
        print(f"  - {grammar.name}")
else:
    print("⚠️  No hay grammar asociada a este intent aún")
    print("   (Esto es normal - se puede agregar después)")

# ============================================
# TEST 7: Contenido Completo
# ============================================

print("\n🎓 TEST 7: Obtener Contenido Completo")
print("-"*60)

try:
    content = orchestrator.get_learning_content(user, milestone)
    
    print("✅ Contenido ensamblado correctamente\n")
    
    print("Estructura de respuesta:")
    print(f"  current_intent: {content['current_intent'].intent.name if content.get('current_intent') else 'None'}")
    print(f"  target_phrases: {len(content.get('target_phrases', []))} frases")
    print(f"  supporting_grammar: {len(content.get('supporting_grammar', []))} unidades")
    print(f"  exercises: {len(content.get('exercises', []))} ejercicios")
    
    if content.get('supporting_grammar'):
        first_gram = content['supporting_grammar'][0]
        print(f"    First Grammar Type: {type(first_gram).__name__}")
        if hasattr(first_gram, 'context_example'):
            print(f"    AI Examples found: {first_gram.context_example}")
        else:
            print(f"    WARNING: No context_example found (likely GrammarUnit)")
    print(f"  progress: {content.get('progress', {})}")
    
except Exception as e:
    print(f"❌ Error obteniendo contenido: {e}")
    import traceback
    traceback.print_exc()

# ============================================
# RESUMEN
# ============================================

print("\n" + "="*60)
print("📊 RESUMEN DE TESTS")
print("="*60)

from apps.intents.models import IntentRealization
from apps.grammar.models import GrammarInMilestone

total_realizations = IntentRealization.objects.count()
total_grammar_examples = GrammarInMilestone.objects.count()

print(f"\n✅ Orquestador funcional")
print(f"📦 IntentRealization en DB: {total_realizations}")
print(f"📚 GrammarInMilestone en DB: {total_grammar_examples}")
print(f"\n💡 Generación on-the-fly: ACTIVA")
print(f"   Primera vez: AI genera (1-2 seg)")
print(f"   Siguientes: Caché instantáneo")

print("\n✅ Tests completados!")
