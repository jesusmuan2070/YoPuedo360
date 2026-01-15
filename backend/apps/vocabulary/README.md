# Vocabulary App

Sistema de gestión de vocabulario con **arquitectura de 4 capas** para YoPuedo360.

---

## 📊 Arquitectura

Este app implementa la **CAPA 1 (Content)** y **CAPA 2 (Application)** de la arquitectura:

```
CAPA 1: Content (Universal)
└─ Vocabulary: Palabra vive 1 vez

CAPA 2: Application (Contexto)
└─ VocabularyInMilestone: Conecta palabra con milestone específico

CAPA 3: Practice (Ejercicios)
└─ ExerciseGenerator usa VocabularyInMilestone

CAPA 4: User State (Progreso)
└─ UserVocabularyProgress trackea avance SRS
```

---

## 🗂️ Modelos

### 1. `Vocabulary` (Capa 1)

**Palabra universal** - Vive 1 vez en el sistema.

```python
Vocabulary(
    word='coffee',
    lemma='coffee',
    level='A1',
    part_of_speech='noun',
    morphological_forms={
        'singular': 'coffee',
        'plural': 'coffees'
    },
    definition_en='A hot drink made from roasted beans',
    definition_es='Bebida caliente hecha de granos tostados',
    phonetic='/ˈkɔː.fi/',
    source='cambridge'
)
```

**Campos clave:**
- `word`: Palabra exacta (unique)
- `lemma`: Forma base (indexado)
- `level`: A1-C2 (CEFR)
- `morphological_forms`: Formas auto-generadas (Pattern.en)
- `source`: oxford, cambridge, manual

**Métodos:**
- `get_form(form_name)`: Obtiene forma morfológica específica

---

### 2. `VocabularyInMilestone` (Capa 2)

**Conexión contextualizada** entre vocabulario y milestone.

```python
VocabularyInMilestone(
    vocabulary=coffee,              # FK a Vocabulary
    milestone=order_food_milestone, # FK a Milestone
    context_usage='Can I have a coffee, please?',
    importance_weight=5,            # 1-5 (crítico)
    is_active_target=True,          # Producción vs comprensión
    introduction_order=1            # Orden de enseñanza
)
```

**Características:**
- Misma palabra puede estar en **múltiples milestones** con diferentes contextos
- `introduction_order` es **independiente por milestone**
- Ordering automático por `introduction_order` en queries

**Ejemplo:**

```python
# "please" en 3 milestones diferentes
Restaurant → Order food: please (order=5, context="Can I have coffee, please?")
Airport → Check-in: please (order=2, context="Can I see your passport, please?")
Hotel → Check-in: please (order=1, context="Can I check in, please?")
```

---

### 3. `VocabularyUsage` (LEGACY - Deprecado)

⚠️ **NO usar en código nuevo.** Conecta a Scenario (muy alto nivel). Usar `VocabularyInMilestone`.

---

### 4. `UserVocabularyProgress` (Capa 4)

Sistema de **Spaced Repetition (SRS)** por usuario.

**Algoritmo:** SM-2 (similar a Anki)

**Campos:**
- `ease_factor`: Multiplicador de intervalo
- `interval`: Días hasta próximo repaso
- `status`: new, learning, review, mastered

**Métodos:**
- `process_review(quality)`: Procesa resultado de repaso (0-5)
- `get_words_for_review(user, limit)`: Palabras pendientes hoy
- `get_vocabulary_stats(user)`: Estadísticas del usuario

---

## 💾 Fuentes de Datos

| Source | Cómo se obtiene | Campos |
|--------|----------------|--------|
| **Cambridge Profile** | Wordlist A1-C2 (gratis) | word, level, frequency |
| **Oxford 3000/5000** | API (licencia $5k/año) | + phonetic, audio, definition |
| **Pattern.en** | Auto-generación | morphological_forms |
| **spaCy** | Auto-detección | part_of_speech, lemma |
| **Manual** | Django Admin | Palabras custom |

---

## 🧪 Testing

**9 tests con múltiples scenarios** (Pesticide Paradox):

```bash
pytest apps/vocabulary/ -v
```

**Tests:**
- ✅ Misma palabra en múltiples milestones con orden diferente
- ✅ Ordering con gaps (1, 5, 10, 100)
- ✅ Niveles CEFR mezclados en mismo milestone
- ✅ Unique constraint evita duplicados
- ✅ Filtrado por importance_weight
- ✅ Active vs passive vocabulary
- ✅ Contextos diferentes por milestone
- ✅ Método get_form()
- ✅ Performance con 500 registros

**Cobertura:** ~95% de modelos y métodos principales

---

## 🔗 Flujo de Uso

### 1. Seed Vocabulario Universal (1 vez)

```python
# Script: scripts/seed_vocabulary.py
from pattern.en import conjugate
import spacy

nlp = spacy.load("en_core_web_sm")

for word_data in CAMBRIDGE_A1_WORDS:
    vocab = Vocabulary.objects.create(
        word=word_data['word'],
        lemma=nlp(word_data['word'])[0].lemma_,
        level=word_data['level'],
        morphological_forms=generate_forms(word_data['word']),
        source='cambridge'
    )
```

### 2. Conectar a Milestones

```python
# En seed de scenarios
VocabularyInMilestone.objects.create(
    vocabulary=Vocabulary.objects.get(word='coffee'),
    milestone=restaurant_milestone,
    context_usage='Can I have a coffee?',
    importance_weight=5,
    introduction_order=1
)
```

### 3. Obtener Vocabulario de un Milestone

```python
# En API/views
milestone = Milestone.objects.get(id=milestone_id)
vocab_items = milestone.vocabulary_items.all()  # Ya ordenado por introduction_order

# Filtrar solo crítico
critical_vocab = milestone.vocabulary_items.filter(importance_weight__gte=4)

# Solo vocabulario activo
active_vocab = milestone.vocabulary_items.filter(is_active_target=True)
```

### 4. Trackear Progreso del Usuario

```python
# Cuando usuario practica
from apps.vocabulary.models import UserVocabularyProgress

progress = UserVocabularyProgress.objects.get(
    user=user,
    vocabulary=vocab
)

progress.process_review(quality=4)  # 0-5 (similar a Anki)

# Obtener palabras para repasar hoy
words_to_review = UserVocabularyProgress.get_words_for_review(user, limit=20)
```

---

## ✅ Completado

- [x] Modelo `Vocabulary` con campos NLP
- [x] Modelo `VocabularyInMilestone` para contexto
- [x] Método `get_form()` para formas morfológicas
- [x] Migrations aplicadas
- [x] Tests comprehensivos (9 tests, todos pasan)
- [x] Deprecar `VocabularyUsage`
- [x] SRS implementado con algoritmo SM-2
- [x] Documentación completa

---

## ⏭️ Pendiente

### Alta Prioridad

- [ ] **Script de seed**: `scripts/seed_vocabulary.py`
  - Cargar Cambridge A1-A2 (~700 palabras)
  - Auto-generar morphological_forms con Pattern.en
  - Auto-detectar POS con spaCy

- [ ] **Seed de conexiones**: Conectar vocabulary a milestones existentes
  - Restaurant → 20 palabras
  - Airport → 20 palabras
  - Hotel → 20 palabras

### Media Prioridad

- [ ] **API endpoints**:
  - `GET /milestones/{id}/vocabulary/` - Obtener vocabulario del milestone
  - `GET /vocabulary/review/` - Palabras pendientes de repaso
  - `POST /vocabulary/{id}/review/` - Procesar repaso

- [ ] **Admin enhancements**:
  - Inline VocabularyInMilestone en Milestone admin
  - Filtros por level, source, importance_weight

### Baja Prioridad

- [ ] **Arreglar unique constraint**: `word` + `part_of_speech` (actualmente solo `word`)
- [ ] **Arreglar frequency_rank**: Cambiar default=0 a null=True
- [ ] **Audio generation**: Script para generar audio con Google TTS
- [ ] **Oxford API integration**: Si se obtiene licencia

---

## 📁 Estructura de Archivos

```
apps/vocabulary/
├── __init__.py
├── apps.py
├── models.py          # Vocabulary, VocabularyInMilestone, UserVocabularyProgress
├── admin.py           # Admin configurado
├── tests.py           # 9 tests (todos pasan)
└── README.md          # Este archivo
```

---

## 🔍 Queries Útiles

```python
# 1. Vocabulario de un milestone ordenado
milestone.vocabulary_items.all()

# 2. Solo palabras críticas
milestone.vocabulary_items.filter(importance_weight=5)

# 3. Palabras que usuario debe PRODUCIR
milestone.vocabulary_items.filter(is_active_target=True)

# 4. Cuántas veces se usa "please" en milestones
please = Vocabulary.objects.get(word='please')
please.milestone_usages.count()

# 5. Todos los milestones que usan "coffee"
coffee = Vocabulary.objects.get(word='coffee')
coffee.milestone_usages.select_related('milestone')

# 6. Estadísticas del usuario
UserVocabularyProgress.get_vocabulary_stats(user)
# → {'total': 150, 'mastered': 45, 'learning': 60, 'new': 45}
```

---

## 🎯 Decisiones de Diseño

### ¿Por qué Vocabulary es universal?

**Alternativa rechazada:** Crear palabra por milestone
```python
# ❌ Mala arquitectura
Milestone.vocabulary = JSONField(['coffee', 'water'])
```

**Problemas:**
- Duplicación: "coffee" en 20 milestones = 20 copias
- Progreso fragmentado: Usuario aprende "coffee" 20 veces separadas
- Difícil de mantener: Cambiar traducción requiere actualizar 20 lugares

**Arquitectura elegida:**
```python
# ✅ Buena arquitectura
coffee = Vocabulary (1 vez)
VocabularyInMilestone conecta coffee a 20 milestones
```

**Beneficios:**
- 0 duplicación
- Progreso unificado
- Mantenimiento simple

### ¿Por qué introduction_order por milestone?

Cada milestone tiene su secuencia pedagógica independiente:

```
Restaurant:
1. coffee
2. water
3. menu

Airport:
1. plane
2. passport
3. please  ← Misma palabra pero orden diferente
```

---

## 📞 Soporte

Para dudas sobre este app, revisar:
1. Este README
2. Tests en `tests.py` (ejemplos de uso)
3. Plan de arquitectura: `brain/final_architecture_plan.md`
