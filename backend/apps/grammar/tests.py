"""
Grammar Tests - Pytest version
Tests with multiple scenarios and edge cases (Pesticide Paradox)
"""
import pytest
import time
from apps.grammar.models import GrammarUnit, GrammarInMilestone, UserGrammarProgress
from apps.scenarios.models import Scenario, Milestone


# ============================================
# FIXTURES (reutilizables)
# ============================================

@pytest.fixture
def grammar_units():
    """Grammar units universales reutilizables"""
    return {
        'can_infinitive': GrammarUnit.objects.create(
            slug='can-infinitive',
            name='Can + Infinitive',
            level='A1',
            grammatical_category='modal_verb',
            form='can + base verb',
            meaning_en='Ability, permission, possibility',
            meaning_es='Habilidad, permiso, posibilidad',
            pedagogical_sequence=1,
            is_universal=True
        ),
        'a_an': GrammarUnit.objects.create(
            slug='a-an-articles',
            name='A/An Articles',
            level='A1',
            grammatical_category='article',
            form='a + consonant sound, an + vowel sound',
            meaning_en='Indefinite articles',
            meaning_es='Artículos indefinidos',
            pedagogical_sequence=2
        ),
        'present_simple': GrammarUnit.objects.create(
            slug='present-simple',
            name='Present Simple',
            level='A1',
            grammatical_category='tense',
            form='subject + verb (+ s for 3rd person)',
            meaning_en='Habitual actions, facts',
            meaning_es='Acciones habituales, hechos',
            pedagogical_sequence=3
        ),
        'could_infinitive': GrammarUnit.objects.create(
            slug='could-infinitive',
            name='Could + Infinitive',
            level='A2',
            grammatical_category='modal_verb',
            form='could + base verb',
            meaning_en='Past ability, polite request',
            meaning_es='Habilidad pasada, petición cortés',
            pedagogical_sequence=10
        ),
    }


@pytest.fixture
def scenarios():
    """Múltiples scenarios"""
    return {
        'restaurant': Scenario.objects.create(slug='restaurant', name='Restaurant', icon='☕'),
        'airport': Scenario.objects.create(slug='airport', name='Airport', icon='✈️'),
        'hotel': Scenario.objects.create(slug='hotel', name='Hotel', icon='🏨'),
    }


@pytest.fixture
def milestones(scenarios):
    """Múltiples milestones en diferentes scenarios"""
    return {
        'order_food': Milestone.objects.create(
            scenario=scenarios['restaurant'], level='A1', order=3, name='Order food'
        ),
        'checkin': Milestone.objects.create(
            scenario=scenarios['airport'], level='A1', order=1, name='Check-in'
        ),
        'hotel_checkin': Milestone.objects.create(
            scenario=scenarios['hotel'], level='A1', order=1, name='Hotel check-in'
        ),
    }


# ============================================
# TEST 1: Mismo grammar en MÚLTIPLES milestones
# ============================================

@pytest.mark.django_db
def test_same_grammar_different_milestones_different_context(grammar_units, milestones):
    """
    Grammar UNIVERSAL - mismo pattern en múltiples contextos
    
    "can" se usa en 3 milestones con diferentes ejemplos
    """
    # "can" en Restaurant
    GrammarInMilestone.objects.create(
        grammar=grammar_units['can_infinitive'],
        milestone=milestones['order_food'],
        context_example='Can I have a coffee?',
        importance_weight=5,
        introduction_order=1
    )
    
    # "can" en Airport (MISMO grammar)
    GrammarInMilestone.objects.create(
        grammar=grammar_units['can_infinitive'],
        milestone=milestones['checkin'],
        context_example='Can I see your passport?',
        importance_weight=5,
        introduction_order=1
    )
    
    # "can" en Hotel (MISMO grammar)
    GrammarInMilestone.objects.create(
        grammar=grammar_units['can_infinitive'],
        milestone=milestones['hotel_checkin'],
        context_example='Can I check in?',
        importance_weight=4,
        introduction_order=1
    )
    
    # Verificar que REUTILIZA el mismo grammar
    can_grammar = grammar_units['can_infinitive']
    usages = can_grammar.milestone_usages.all()
    
    assert usages.count() == 3
    assert usages[0].context_example == 'Can I have a coffee?'
    assert usages[1].context_example == 'Can I see your passport?'
    assert usages[2].context_example == 'Can I check in?'


# ============================================
# TEST 2: Ordering con GAPS
# ============================================

@pytest.mark.django_db
def test_ordering_with_gaps(grammar_units, milestones):
    """¿Qué pasa si hay gaps en introduction_order? (1, 5, 10)"""
    # Crear con gaps
    GrammarInMilestone.objects.create(
        grammar=grammar_units['can_infinitive'],
        milestone=milestones['order_food'],
        introduction_order=1
    )
    GrammarInMilestone.objects.create(
        grammar=grammar_units['a_an'],
        milestone=milestones['order_food'],
        introduction_order=5
    )
    GrammarInMilestone.objects.create(
        grammar=grammar_units['present_simple'],
        milestone=milestones['order_food'],
        introduction_order=10
    )
    
    items = list(milestones['order_food'].grammar_items.all())
    
    # Debe ordenar correctamente a pesar de gaps
    assert items[0].introduction_order == 1
    assert items[1].introduction_order == 5
    assert items[2].introduction_order == 10
    assert len(items) == 3


# ============================================
# TEST 3: Niveles mezclados en mismo milestone
# ============================================

@pytest.mark.django_db
def test_mixed_cefr_levels_in_milestone(grammar_units, milestones):
    """
    Milestone A1 puede tener grammar A2 para contexto/comprensión
    """
    GrammarInMilestone.objects.create(
        grammar=grammar_units['can_infinitive'],  # A1
        milestone=milestones['order_food'],
        is_primary_focus=True,
        introduction_order=1
    )
    
    GrammarInMilestone.objects.create(
        grammar=grammar_units['could_infinitive'],  # A2 (más avanzado)
        milestone=milestones['order_food'],
        is_primary_focus=False,  # Solo para comprensión
        introduction_order=2
    )
    
    items = milestones['order_food'].grammar_items.all()
    
    assert items.count() == 2
    assert items[0].grammar.level == 'A1'
    assert items[1].grammar.level == 'A2'
    assert items[0].is_primary_focus is True
    assert items[1].is_primary_focus is False


# ============================================
# TEST 4: Unique constraint
# ============================================

@pytest.mark.django_db
def test_cannot_add_same_grammar_twice_to_milestone(grammar_units, milestones):
    """¿Evita duplicados? (grammar + milestone debe ser único)"""
    from django.db import IntegrityError
    
    GrammarInMilestone.objects.create(
        grammar=grammar_units['can_infinitive'],
        milestone=milestones['order_food'],
        introduction_order=1
    )
    
    # Intentar agregar la misma combinación
    with pytest.raises(IntegrityError):
        GrammarInMilestone.objects.create(
            grammar=grammar_units['can_infinitive'],
            milestone=milestones['order_food'],  # ← Mismo
            introduction_order=2
        )


# ============================================
# TEST 5: Filtrado por importance_weight
# ============================================

@pytest.mark.django_db
def test_filter_by_importance(grammar_units, milestones):
    """¿Puedo obtener solo grammar crítico de un milestone?"""
    GrammarInMilestone.objects.create(
        grammar=grammar_units['can_infinitive'],
        milestone=milestones['order_food'],
        importance_weight=5,  # Crítico
        introduction_order=1
    )
    
    GrammarInMilestone.objects.create(
        grammar=grammar_units['a_an'],
        milestone=milestones['order_food'],
        importance_weight=3,  # Normal
        introduction_order=2
    )
    
    GrammarInMilestone.objects.create(
        grammar=grammar_units['present_simple'],
        milestone=milestones['order_food'],
        importance_weight=1,  # Opcional
        introduction_order=3
    )
    
    # Obtener solo grammar crítico (importance >= 4)
    critical = milestones['order_food'].grammar_items.filter(importance_weight__gte=4)
    
    assert critical.count() == 1
    assert critical[0].grammar.name == 'Can + Infinitive'


# ============================================
# TEST 6: Primary focus vs secondary
# ============================================

@pytest.mark.django_db
def test_primary_vs_secondary_focus(grammar_units, milestones):
    """¿Puedo distinguir grammar objetivo vs auxiliar?"""
    GrammarInMilestone.objects.create(
        grammar=grammar_units['can_infinitive'],
        milestone=milestones['order_food'],
        is_primary_focus=True,  # Objetivo principal
        introduction_order=1
    )
    
    GrammarInMilestone.objects.create(
        grammar=grammar_units['a_an'],
        milestone=milestones['order_food'],
        is_primary_focus=False,  # Auxiliar
        introduction_order=2
    )
    
    # Obtener solo grammar objetivo
    primary = milestones['order_food'].grammar_items.filter(is_primary_focus=True)
    secondary = milestones['order_food'].grammar_items.filter(is_primary_focus=False)
    
    assert primary.count() == 1
    assert secondary.count() == 1
    assert primary[0].grammar.name == 'Can + Infinitive'


# ============================================
# TEST 7: SRS - process_review
# ============================================

@pytest.mark.django_db
def test_user_grammar_progress_srs(grammar_units, django_user_model):
    """¿SRS funciona igual que Vocabulary?"""
    user = django_user_model.objects.create_user(username='testuser', password='pass')
    
    progress = UserGrammarProgress.objects.create(
        user=user,
        grammar=grammar_units['can_infinitive']
    )
    
    # Inicial
    assert progress.status == 'new'
    assert progress.repetitions == 0
    
    # Review correcto (quality=5)
    progress.process_review(quality=5)
    
    assert progress.status == 'review'  # Después de 1 repetición correcta → review
    assert progress.repetitions == 1
    assert progress.times_correct == 1
    assert progress.interval == 1  # Primer intervalo


# ============================================
# TEST 8: get_grammar_for_review
# ============================================

@pytest.mark.django_db
def test_get_grammar_for_review(grammar_units, django_user_model):
    """¿Puedo obtener grammar que necesita repaso hoy?"""
    from datetime import date, timedelta
    
    user = django_user_model.objects.create_user(username='testuser', password='pass')
    
    # Grammar que necesita review HOY
    UserGrammarProgress.objects.create(
        user=user,
        grammar=grammar_units['can_infinitive'],
        next_review=date.today()
    )
    
    # Grammar que NO necesita review (futuro)
    UserGrammarProgress.objects.create(
        user=user,
        grammar=grammar_units['a_an'],
        next_review=date.today() + timedelta(days=7)
    )
    
    # Obtener solo los que necesitan review hoy
    due_today = UserGrammarProgress.get_grammar_for_review(user, limit=10)
    
    assert due_today.count() == 1
    assert due_today[0].grammar.slug == 'can-infinitive'


# ============================================
# BONUS: Performance test
# ============================================

@pytest.mark.django_db
def test_query_performance_many_milestones(scenarios):
    """¿Qué pasa con MUCHO grammar en MUCHOS milestones?"""
    # Crear 50 grammar units
    grammars = [
        GrammarUnit.objects.create(
            slug=f'grammar-{i}',
            name=f'Grammar {i}',
            level='A1',
            grammatical_category='modal_verb',
            form=f'form {i}',
            meaning_en=f'meaning {i}',
            meaning_es=f'significado {i}',
            pedagogical_sequence=i
        ) for i in range(50)
    ]
    
    # Crear 10 milestones
    milestones = [
        Milestone.objects.create(
            scenario=scenarios['restaurant'],
            level='A1',
            order=i,
            name=f'Milestone {i}'
        ) for i in range(10)
    ]
    
    # Conectar 20 grammars a cada milestone
    for milestone in milestones:
        for i, grammar in enumerate(grammars[:20]):
            GrammarInMilestone.objects.create(
                grammar=grammar,
                milestone=milestone,
                introduction_order=i+1
            )
    
    # Test: ¿Query es rápido?
    start = time.time()
    items = milestones[0].grammar_items.all()
    list(items)  # Force evaluation
    elapsed = time.time() - start
    
    # Debe ser < 100ms
    assert elapsed < 0.1, f"Query tardó {elapsed}s, muy lento!"
    assert items.count() == 20
