"""
Vocabulary Tests - Pytest version
Tests con múltiples scenarios y edge cases (Pesticide Paradox)
"""
import pytest
import time
from apps.vocabulary.models import Vocabulary, VocabularyInMilestone
from apps.scenarios.models import Scenario, Milestone


# ============================================
# FIXTURES (reutilizables)
# ============================================

@pytest.fixture
def vocabularies():
    """Vocabulario universal reutilizable"""
    return {
        'please': Vocabulary.objects.create(
            word='please', lemma='please', level='A1', part_of_speech='adverb'
        ),
        'coffee': Vocabulary.objects.create(
            word='coffee', lemma='coffee', level='A1', part_of_speech='noun'
        ),
        'passport': Vocabulary.objects.create(
            word='passport', lemma='passport', level='A1', part_of_speech='noun'
        ),
        'luggage': Vocabulary.objects.create(
            word='luggage', lemma='luggage', level='A2', part_of_speech='noun'
        ),
        'procrastinate': Vocabulary.objects.create(
            word='procrastinate', lemma='procrastinate', level='C1', part_of_speech='verb'
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
# TEST 1: Misma palabra en MÚLTIPLES milestones
# ============================================

@pytest.mark.django_db
def test_same_word_different_milestones_different_order(vocabularies, milestones):
    """
    Bug potencial: ¿"please" puede tener introduction_order diferente 
    en cada milestone?
    
    Pesticide Paradox: Testing con 3 scenarios diferentes
    """
    # "please" en Restaurant (5ta palabra)
    VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['please'],
        milestone=milestones['order_food'],
        context_usage='Can I have coffee, please?',
        introduction_order=5
    )
    
    # "please" en Airport (2da palabra)
    VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['please'],
        milestone=milestones['checkin'],
        context_usage='Can I see your passport, please?',
        introduction_order=2
    )
    
    # "please" en Hotel (1ra palabra)
    VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['please'],
        milestone=milestones['hotel_checkin'],
        context_usage='Can I check in, please?',
        introduction_order=1
    )
    
    # Verificar que cada milestone tiene SU PROPIO orden
    restaurant_please = milestones['order_food'].vocabulary_items.get(
        vocabulary=vocabularies['please']
    )
    airport_please = milestones['checkin'].vocabulary_items.get(
        vocabulary=vocabularies['please']
    )
    hotel_please = milestones['hotel_checkin'].vocabulary_items.get(
        vocabulary=vocabularies['please']
    )
    
    assert restaurant_please.introduction_order == 5
    assert airport_please.introduction_order == 2
    assert hotel_please.introduction_order == 1


# ============================================
# TEST 2: Ordering con GAPS (no consecutivo)
# ============================================

@pytest.mark.django_db
def test_ordering_with_gaps(vocabularies, milestones):
    """¿Qué pasa si hay gaps en introduction_order? (1, 5, 10, 100)"""
    water = Vocabulary.objects.create(word='water', lemma='water', level='A1')
    menu = Vocabulary.objects.create(word='menu', lemma='menu', level='A1')
    bill = Vocabulary.objects.create(word='bill', lemma='bill', level='A2')
    
    # Crear con gaps grandes
    VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['coffee'],
        milestone=milestones['order_food'],
        introduction_order=1
    )
    VocabularyInMilestone.objects.create(
        vocabulary=water,
        milestone=milestones['order_food'],
        introduction_order=5
    )
    VocabularyInMilestone.objects.create(
        vocabulary=menu,
        milestone=milestones['order_food'],
        introduction_order=10
    )
    VocabularyInMilestone.objects.create(
        vocabulary=bill,
        milestone=milestones['order_food'],
        introduction_order=100
    )
    
    items = list(milestones['order_food'].vocabulary_items.all())
    
    # Debe ordenar correctamente a pesar de gaps
    assert items[0].introduction_order == 1
    assert items[1].introduction_order == 5
    assert items[2].introduction_order == 10
    assert items[3].introduction_order == 100
    assert len(items) == 4


# ============================================
# TEST 3: Palabras de DIFERENTES niveles en mismo milestone
# ============================================

@pytest.mark.django_db
def test_mixed_cefr_levels_in_milestone(vocabularies, milestones):
    """
    Edge case: ¿Milestone A1 puede tener palabras A2, B1, C1?
    (Respuesta: SÍ, para contexto/comprensión pasiva)
    """
    VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['coffee'],  # A1
        milestone=milestones['order_food'],
        is_active_target=True,  # Usuario debe decirla
        introduction_order=1
    )
    
    VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['luggage'],  # A2 (más difícil)
        milestone=milestones['order_food'],
        is_active_target=False,  # Solo reconocerla
        introduction_order=2
    )
    
    VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['procrastinate'],  # C1 (muy difícil)
        milestone=milestones['order_food'],
        is_active_target=False,  # Solo comprensión
        introduction_order=3
    )
    
    items = milestones['order_food'].vocabulary_items.all()
    
    # Debe permitir mezcla de niveles
    assert items.count() == 3
    assert items[0].vocabulary.level == 'A1'
    assert items[1].vocabulary.level == 'A2'
    assert items[2].vocabulary.level == 'C1'


# ============================================
# TEST 4: Unique constraint
# ============================================

@pytest.mark.django_db
def test_cannot_add_same_vocab_twice_to_milestone(vocabularies, milestones):
    """¿Evita duplicados? (vocabulary + milestone debe ser único)"""
    from django.db import IntegrityError
    
    VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['coffee'],
        milestone=milestones['order_food'],
        introduction_order=1
    )
    
    # Intentar agregar la misma combinación
    with pytest.raises(IntegrityError):
        VocabularyInMilestone.objects.create(
            vocabulary=vocabularies['coffee'],
            milestone=milestones['order_food'],  # ← Misma combinación
            introduction_order=2  # Aunque el orden sea diferente
        )


# ============================================
# TEST 5: Filtrado por importance_weight
# ============================================

@pytest.mark.django_db
def test_filter_by_importance(vocabularies, milestones):
    """¿Puedo obtener solo vocabulario crítico de un milestone?"""
    VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['coffee'],
        milestone=milestones['order_food'],
        importance_weight=5,  # Crítico
        introduction_order=1
    )
    
    water = Vocabulary.objects.create(word='water', lemma='water', level='A1')
    VocabularyInMilestone.objects.create(
        vocabulary=water,
        milestone=milestones['order_food'],
        importance_weight=3,  # Normal
        introduction_order=2
    )
    
    napkin = Vocabulary.objects.create(word='napkin', lemma='napkin', level='A2')
    VocabularyInMilestone.objects.create(
        vocabulary=napkin,
        milestone=milestones['order_food'],
        importance_weight=1,  # Opcional
        introduction_order=3
    )
    
    # Obtener solo vocabulario crítico (importance >= 4)
    critical = milestones['order_food'].vocabulary_items.filter(importance_weight__gte=4)
    
    assert critical.count() == 1
    assert critical[0].vocabulary.word == 'coffee'


# ============================================
# TEST 6: Active vs Passive vocabulary
# ============================================

@pytest.mark.django_db
def test_active_vs_passive_target(vocabularies, milestones):
    """¿Puedo distinguir qué debe producir vs solo reconocer?"""
    VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['coffee'],
        milestone=milestones['order_food'],
        is_active_target=True,  # Debe poder decir
        introduction_order=1
    )
    
    VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['luggage'],
        milestone=milestones['order_food'],
        is_active_target=False,  # Solo reconocer
        introduction_order=2
    )
    
    # Obtener solo vocabulario activo
    active = milestones['order_food'].vocabulary_items.filter(is_active_target=True)
    passive = milestones['order_food'].vocabulary_items.filter(is_active_target=False)
    
    assert active.count() == 1
    assert passive.count() == 1
    assert active[0].vocabulary.word == 'coffee'


# ============================================
# TEST 7: Context usage específico por milestone
# ============================================

@pytest.mark.django_db
def test_different_context_usage_per_milestone(vocabularies, milestones):
    """Misma palabra, diferentes contextos según milestone"""
    # "coffee" en Restaurant
    restaurant_vim = VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['coffee'],
        milestone=milestones['order_food'],
        context_usage='Can I have a coffee, please?',
        introduction_order=1
    )
    
    # "coffee" en Hotel (diferente contexto)
    hotel_vim = VocabularyInMilestone.objects.create(
        vocabulary=vocabularies['coffee'],
        milestone=milestones['hotel_checkin'],
        context_usage='Is there coffee in the room?',
        introduction_order=3
    )
    
    assert restaurant_vim.context_usage != hotel_vim.context_usage
    assert 'Can I have' in restaurant_vim.context_usage
    assert 'room' in hotel_vim.context_usage


# ============================================
# TEST 8: Vocabulary.get_form() method
# ============================================

@pytest.mark.django_db
def test_vocabulary_get_form_method():
    """¿El método get_form() devuelve formas morfológicas correctamente?"""
    swim = Vocabulary.objects.create(
        word='swim',
        lemma='swim',
        level='A1',
        part_of_speech='verb',
        morphological_forms={
            'present': 'swim',
            'past': 'swam',
            'past_participle': 'swum',
            'gerund': 'swimming',
            'third_person': 'swims'
        }
    )
    
    # Obtener formas específicas
    assert swim.get_form('past') == 'swam'
    assert swim.get_form('gerund') == 'swimming'
    assert swim.get_form('third_person') == 'swims'
    
    # Forma que no existe → devuelve palabra original
    assert swim.get_form('nonexistent') == 'swim'


# ============================================
# BONUS: Test de performance
# ============================================

@pytest.mark.django_db
def test_query_performance_with_many_milestones(scenarios):
    """¿Qué pasa con MUCHOS milestones y MUCHO vocabulario?"""
    # Crear 100 vocabularios
    vocabs = [
        Vocabulary.objects.create(
            word=f'word{i}',
            lemma=f'word{i}',
            level='A1'
        ) for i in range(100)
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
    
    # Conectar 50 palabras a cada milestone
    for milestone in milestones:
        for i, vocab in enumerate(vocabs[:50]):
            VocabularyInMilestone.objects.create(
                vocabulary=vocab,
                milestone=milestone,
                introduction_order=i+1
            )
    
    # Test: ¿Query es rápido?
    start = time.time()
    items = milestones[0].vocabulary_items.all()
    list(items)  # Force evaluation
    elapsed = time.time() - start
    
    # Debe ser < 100ms
    assert elapsed < 0.1, f"Query tardó {elapsed}s, muy lento!"
    assert items.count() == 50
