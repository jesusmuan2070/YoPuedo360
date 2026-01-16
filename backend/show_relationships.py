"""
Script para inspeccionar relaciones de modelos en Django shell

Ejecutar con:
python manage.py shell < show_relationships.py
"""

from apps.vocabulary.models import Vocabulary, VocabularyInMilestone, UserVocabularyProgress
from apps.grammar.models import GrammarUnit, GrammarInMilestone, UserGrammarProgress
from apps.scenarios.models import Scenario, Milestone

print("\n" + "="*80)
print("ESTRUCTURA DE BASE DE DATOS - YoPuedo360")
print("="*80 + "\n")

def show_model_info(model_class):
    """Muestra información de un modelo y sus relaciones"""
    print(f"\n📦 {model_class.__name__}")
    print("-" * 60)
    
    # Mostrar campos
    print("\n  Campos:")
    for field in model_class._meta.get_fields():
        field_type = field.__class__.__name__
        
        if field_type == 'ForeignKey':
            print(f"    • {field.name} → {field.related_model.__name__} (FK)")
        elif field_type == 'ManyToOneRel':
            print(f"    • {field.name} ← {field.related_model.__name__} (reverse FK)")
        elif field_type in ['CharField', 'TextField', 'IntegerField', 'BooleanField', 'DateField', 'FloatField', 'JSONField']:
            print(f"    • {field.name} ({field_type})")
    
    # Contar registros
    try:
        count = model_class.objects.count()
        print(f"\n  📊 Registros en DB: {count}")
    except:
        print(f"\n  📊 Registros en DB: (tabla no existe todavía)")

print("\n" + "🔵 CAPA 1: CONTENIDO UNIVERSAL")
print("="*80)
show_model_info(Vocabulary)
show_model_info(GrammarUnit)

print("\n" + "🟢 CAPA 2: ESCENARIOS Y CONTEXTUALIZACIÓN")
print("="*80)
show_model_info(Scenario)
show_model_info(Milestone)
show_model_info(VocabularyInMilestone)
show_model_info(GrammarInMilestone)

print("\n" + "🟡 CAPA 4: PROGRESO DE USUARIOS")
print("="*80)
show_model_info(UserVocabularyProgress)
show_model_info(UserGrammarProgress)

print("\n" + "="*80)
print("EJEMPLOS DE QUERIES")
print("="*80 + "\n")

print("1. Obtener todos los milestones de Restaurant:")
print("   Milestone.objects.filter(scenario__slug='restaurant')")

print("\n2. Obtener vocabulario del milestone 'Order food':")
print("   milestone = Milestone.objects.get(name='Order food')")
print("   milestone.vocabulary_items.all()")

print("\n3. Ver dónde se usa la palabra 'coffee':")
print("   coffee = Vocabulary.objects.get(word='coffee')")
print("   coffee.milestone_usages.all()  # Todos los VocabularyInMilestone")

print("\n4. Ver en cuántos milestones se usa 'can + infinitive':")
print("   can = GrammarUnit.objects.get(slug='can-infinitive')")
print("   can.milestone_usages.count()")

print("\n5. Progreso de un usuario en vocabulario:")
print("   from django.contrib.auth import get_user_model")
print("   User = get_user_model()")
print("   user = User.objects.first()")
print("   UserVocabularyProgress.objects.filter(user=user)")

print("\n" + "="*80)
print("RELACIONES (FK = Foreign Key)")
print("="*80 + "\n")

relationships = [
    ("Milestone", "scenario_id", "Scenario", "Milestone pertenece a un Scenario"),
    ("VocabularyInMilestone", "vocabulary_id", "Vocabulary", "Conecta palabra universal con milestone"),
    ("VocabularyInMilestone", "milestone_id", "Milestone", "Define contexto de la palabra"),
    ("GrammarInMilestone", "grammar_id", "GrammarUnit", "Conecta grammar universal con milestone"),
    ("GrammarInMilestone", "milestone_id", "Milestone", "Define ejemplo en contexto"),
    ("UserVocabularyProgress", "user_id", "User", "Tracking de palabra por usuario"),
    ("UserVocabularyProgress", "vocabulary_id", "Vocabulary", "Palabra siendo trackeada"),
    ("UserGrammarProgress", "user_id", "User", "Tracking de grammar por usuario"),
    ("UserGrammarProgress", "grammar_id", "GrammarUnit", "Grammar siendo trackeada"),
]

for from_table, fk_field, to_table, description in relationships:
    print(f"  {from_table}.{fk_field} → {to_table}")
    print(f"    {description}\n")

print("="*80)
print("✅ FIN DEL REPORTE")
print("="*80 + "\n")
