"""
Link Grammar Topics to Milestones
Associates each milestone with relevant grammar topics
Run with: python scripts/link_grammar_milestones.py
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
django.setup()

from apps.memory_palace.models import Milestone
from apps.content.models import GrammarTopic, MilestoneGrammar

print("🔗 Linking Grammar to Milestones...")

# ============================================
# MAPEO: Qué gramática se usa en cada tipo de milestone
# ============================================

# Mapeo por palabras clave en el nombre del milestone
GRAMMAR_KEYWORDS = {
    # Verb TO BE
    'a1-verb-to-be': [
        'presentar', 'describir', 'nombre', 'profesional', 
        'conocer', 'saludos', 'identificar'
    ],
    # Present Simple
    'a1-present-simple': [
        'rutina', 'diario', 'trabajo', 'viv', 'com', 
        'beb', 'hablar', 'escuchar'
    ],
    # Articles
    'a1-articles': [
        'pedir', 'ordenar', 'menu', 'comida', 'bebida',
        'comprar', 'querer'
    ],
    # Can/Can't
    'a1-can-cant': [
        'puede', 'pedir', 'ayuda', 'permiso', 'reserv',
        'solicitar', 'preguntar'
    ],
    # Question Words
    'a1-basic-questions': [
        'preguntar', 'donde', 'cuando', 'como', 'que',
        'informacion', 'direccion', 'ubicacion'
    ],
    # There is/are
    'a1-there-is-are': [
        'hay', 'existe', 'disponible', 'servicio',
        'habitacion', 'mesa'
    ],
    # Imperatives
    'a1-imperatives': [
        'instruccion', 'orden', 'emergencia', 'indicacion',
        'mostrar', 'pasar'
    ],
    # Prepositions
    'a1-prepositions-place': [
        'direccion', 'ubicacion', 'lugar', 'donde',
        'puerta', 'aqui', 'alli'
    ],
    # Possessives
    'a1-possessives': [
        'tu', 'mi', 'su', 'nombre', 'documento',
        'pasaporte', 'reservacion'
    ],
}

# Mapeo por escenario (slugs de escenarios → gramática relevante)
SCENARIO_GRAMMAR = {
    'restaurant': ['a1-can-cant', 'a1-articles', 'a1-basic-questions'],
    'cafe-restaurant': ['a1-can-cant', 'a1-articles', 'a1-basic-questions'],
    'hotel': ['a1-there-is-are', 'a1-can-cant', 'a1-basic-questions'],
    'airport': ['a1-possessives', 'a1-basic-questions', 'a1-imperatives'],
    'greetings': ['a1-verb-to-be', 'a1-possessives', 'a1-basic-questions'],
    'shopping': ['a1-articles', 'a1-demonstratives', 'a1-basic-questions'],
    'transport': ['a1-basic-questions', 'a1-prepositions-place', 'a1-can-cant'],
    'directions': ['a1-prepositions-place', 'a1-imperatives', 'a1-basic-questions'],
    'home': ['a1-there-is-are', 'a1-possessives', 'a1-present-simple'],
    'office': ['a1-present-simple', 'a1-can-cant', 'a1-verb-to-be'],
    'doctor': ['a1-verb-to-be', 'a1-can-cant', 'a1-present-simple'],
    'emergencies': ['a1-imperatives', 'a1-can-cant', 'a1-basic-questions'],
    'job-interview': ['a1-verb-to-be', 'a1-present-simple', 'a1-can-cant'],
    'chat-messaging': ['a1-present-simple', 'a1-basic-questions', 'a1-verb-to-be'],
}

# Cargar todos los topics
grammar_topics = {t.slug: t for t in GrammarTopic.objects.filter(level='A1')}

# Obtener milestones A1
a1_milestones = Milestone.objects.filter(level='A1').select_related('scenario')

links_created = 0

for milestone in a1_milestones:
    milestone_name_lower = milestone.name.lower()
    scenario_slug = milestone.scenario.slug if milestone.scenario else ''
    
    linked_topics = set()
    
    # 1. Buscar por palabras clave en el nombre del milestone
    for topic_slug, keywords in GRAMMAR_KEYWORDS.items():
        for keyword in keywords:
            if keyword in milestone_name_lower:
                linked_topics.add(topic_slug)
                break
    
    # 2. Buscar por escenario
    if scenario_slug in SCENARIO_GRAMMAR:
        for topic_slug in SCENARIO_GRAMMAR[scenario_slug]:
            linked_topics.add(topic_slug)
    
    # 3. Si no hay match, asignar gramática básica
    if not linked_topics:
        linked_topics = {'a1-verb-to-be', 'a1-basic-questions'}
    
    # Crear los vínculos
    is_first = True
    for topic_slug in linked_topics:
        if topic_slug in grammar_topics:
            topic = grammar_topics[topic_slug]
            obj, created = MilestoneGrammar.objects.get_or_create(
                milestone=milestone,
                topic=topic,
                defaults={'is_primary': is_first}
            )
            if created:
                links_created += 1
            is_first = False
    
    print(f"  {milestone.scenario.name if milestone.scenario else '?'} - {milestone.name}: {len(linked_topics)} topics")

print(f"\n🔗 Total links created: {links_created}")
print(f"📊 Milestones with grammar: {MilestoneGrammar.objects.values('milestone').distinct().count()}")
print("\n✅ Grammar linking completed!")
