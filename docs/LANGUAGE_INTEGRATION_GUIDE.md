# Guía de Integración de Nuevos Idiomas

## 📌 Propósito

Este documento sirve como referencia para cuando se integren francés, alemán u otros idiomas al sistema de gramática. Documenta las consideraciones críticas y diferencias morfológicas/sintácticas que deben tenerse en cuenta.

---

## ✅ Estado Actual (2026-01-16)

### Idiomas Soportados
- ✅ **Inglés (en)** - Completamente implementado (16 grammar units A1)
- ⏳ **Francés (fr)** - Modelo preparado, falta seed data
- ⏳ **Alemán (de)** - Modelo preparado, falta seed data

### Modelo GrammarUnit
- ✅ Campo `target_language` implementado
- ✅ Categorías morfológicas expandidas (20 categorías totales)
- ✅ Constraint `unique_together = [['slug', 'target_language']]`
- ✅ Índices optimizados para consultas multi-idioma

---

## 🚨 Diferencias Críticas por Idioma

### Orden Sintáctico (CRÍTICO)

| Idioma | Orden Base | Flexibilidad | Implicaciones |
|--------|-----------|--------------|---------------|
| 🇬🇧 **Inglés** | **SVO** | Rígido | Simple de modelar |
| 🇫🇷 **Francés** | **SVO** | Medio | Pronombres pre-verbales |
| 🇩🇪 **Alemán** | **V2/SOV** | **Alto** | Requiere categoría `word_order` |

#### ⚠️ ALEMÁN: Caso Especial

```python
# El alemán usa V2 (Verb-Second) en oraciones principales
# y SOV en subordinadas

structural_metadata = {
    "word_order": "V2 in main clauses, SOV in subordinate",
    "v2_rule": "El verbo conjugado SIEMPRE va en segunda posición",
    "examples": {
        "main_SVO": "Ich esse Äpfel (I eat apples)",
        "main_VSO_time_first": "Heute esse ich Äpfel (Today eat I apples)",
        "subordinate_SOV": "...dass ich Äpfel esse (...that I apples eat)"
    }
}
```

**Acción Requerida:** Al crear grammar units alemanes, SIEMPRE especificar el orden de palabras en `structural_metadata`.

### Morfología Compleja

#### Francés

| Aspecto | Complejidad | Categoría a Usar |
|---------|-------------|------------------|
| **Género gramatical** | M/F | `gender` |
| **Conjugación verbal** | 12+ tiempos | `tense`, `verb_mood` |
| **Concordancia de adjetivos** | Con género/número | `adjective_agreement` |
| **Pronombres de objeto** | Pre-verbales | `pronoun` |

**Ejemplo de Conjugación Compleja:**
```python
{
    'slug': 'verbe-etre',
    'target_language': 'fr',
    'grammatical_category': 'auxiliary',
    'structural_metadata': {
        "conjugation": {
            "present": {
                "je": "suis", "tu": "es", "il/elle": "est",
                "nous": "sommes", "vous": "êtes", "ils/elles": "sont"
            },
            "passé_composé": {
                "je": "ai été", "tu": "as été", ...
            },
            "imparfait": {...},
            "futur": {...}
            # 12+ tiempos totales
        }
    }
}
```

#### Alemán

| Aspecto | Complejidad | Categoría a Usar |
|---------|-------------|------------------|
| **Género gramatical** | M/F/N (3 géneros) | `gender` |
| **Sistema de casos** | 4 casos (Nom/Akk/Dat/Gen) | `case_system` |
| **Declinación de artículos** | 16 formas (4x4) | `declension` |
| **Orden de palabras** | V2/SOV | `word_order` |

**Ejemplo de Sistema de Casos:**
```python
{
    'slug': 'definite-articles',
    'target_language': 'de',
    'grammatical_category': 'article',
    'structural_metadata': {
        "declension_table": {
            "nominative": {
                "masculine": "der", "feminine": "die", 
                "neuter": "das", "plural": "die"
            },
            "accusative": {
                "masculine": "den", "feminine": "die", 
                "neuter": "das", "plural": "die"
            },
            "dative": {
                "masculine": "dem", "feminine": "der", 
                "neuter": "dem", "plural": "den"
            },
            "genitive": {
                "masculine": "des", "feminine": "der", 
                "neuter": "des", "plural": "der"
            }
        }
    }
}
```

---

## 📋 Checklist para Agregar un Nuevo Idioma

### Pre-requisitos
- [ ] Revisar este documento completo
- [ ] Revisar `apps/grammar/models.py` - categorías disponibles
- [ ] Leer documentos en `.gemini/antigravity/brain/*/`:
  - [ ] `multi_language_grammar_analysis.md`
  - [ ] `word_order_syntax_guide.md`

### Paso 1: Planificación
- [ ] Identificar diferencias morfológicas vs inglés
- [ ] Determinar si se necesitan nuevas categorías en `CATEGORY_CHOICES`
- [ ] Decidir estrategia de slugs (traducidos vs universales)
- [ ] Listar las 10-15 estructuras gramaticales A1 más críticas

### Paso 2: Crear Seed Script
- [ ] Crear archivo `scripts/seed_grammar_a1_[LANG].py`
- [ ] Copiar estructura de `seed_grammar_a1.py` (inglés)
- [ ] Configurar `target_language='[LANG]'`
- [ ] Implementar las estructuras gramaticales específicas

### Paso 3: Estructuras Gramaticales Específicas

#### Para Francés
- [ ] Género gramatical (A1 temprano)
- [ ] Artículos definidos/indefinidos con género
- [ ] Verbe être (presente)
- [ ] Verbe avoir (presente)
- [ ] Présent de l'indicatif (verbos -er)
- [ ] Concordancia de adjetivos
- [ ] Pronombres personales sujeto
- [ ] Négation (ne...pas)
- [ ] Pronombres de objeto directo/indirecto

#### Para Alemán
- [ ] Género gramatical + artículos (A1 **muy temprano**)
- [ ] Sistema de casos - Nominativo (introducción)
- [ ] Verbo sein (presente)
- [ ] Verbo haben (presente)
- [ ] Präsens (verbos regulares)
- [ ] Regla V2 (word_order)
- [ ] Orden SOV en subordinadas
- [ ] Verbos separables
- [ ] Caso Acusativo (objetos directos)

### Paso 4: Validación
- [ ] Ejecutar `python scripts/seed_grammar_a1_[LANG].py`
- [ ] Verificar que todos los items creados tengan prefijo `[LANG]`
- [ ] Revisar en Django Admin que los datos sean correctos
- [ ] Probar queries: `GrammarUnit.objects.filter(target_language='[LANG]')`

### Paso 5: Integración con Milestones
- [ ] Crear/actualizar milestones que usen estas grammar units
- [ ] Usar modelo `GrammarInMilestone` para conectar
- [ ] Verificar que el contexto sea apropiado al idioma

---

## 🎯 Estrategias de Slugs

### Opción A: Slugs Traducidos (Recomendado)
```python
# Inglés
slug='can-infinitive'

# Francés  
slug='pouvoir-infinitif'

# Alemán
slug='koennen-infinitiv'
```

**Ventajas:**
- ✅ Más descriptivo en el idioma target
- ✅ Mejor SEO/URLs si se exponen
- ✅ Autoconsistente con el idioma

### Opción B: Slugs Universales
```python
# Todos los idiomas
slug='modal-can'  # Inglés
slug='modal-can'  # Francés (mismo slug)
slug='modal-can'  # Alemán (mismo slug)
```

**Ventajas:**
- ✅ Más fácil de mapear conceptos equivalentes
- ✅ Queries cross-language más simples

**Decisión:** Se recomienda **Opción A** (traducidos) por claridad pedagógica.

---

## ⚙️ Categorías Disponibles

### Universales (Todos los Idiomas)
- `modal_verb` - Verbos modales
- `article` - Artículos
- `tense` - Tiempos verbales
- `pronoun` - Pronombres
- `preposition` - Preposiciones
- `conjunction` - Conjunciones
- `question_form` - Formación de preguntas
- `negation` - Negación
- `auxiliary` - Verbos auxiliares
- `possessive` - Posesivos
- `comparative` - Comparativos/Superlativos
- `gerund_infinitive` - Gerundios e Infinitivos
- `adverb` - Adverbios
- `adjective` - Adjetivos
- `verb` - Verbos

### Específicas para FR/DE
- `gender` - Género gramatical (FR: M/F, DE: M/F/N)
- `case_system` - Sistema de casos (DE: 4 casos)
- `declension` - Declinación (DE: artículos/adjetivos)
- `verb_mood` - Modos verbales (FR: subjuntivo, condicional)
- `adjective_agreement` - Concordancia de adjetivos (FR)
- `word_order` - Orden de palabras (DE: V2, SOV)

---

## 🔍 Queries Útiles

### Obtener toda la gramática de un idioma
```python
french_grammar = GrammarUnit.objects.filter(target_language='fr')
german_grammar = GrammarUnit.objects.filter(target_language='de')
```

### Gramática A1 por idioma
```python
french_a1 = GrammarUnit.objects.filter(
    target_language='fr',
    level='A1'
).order_by('pedagogical_sequence')
```

### Estructuras específicas de un idioma
```python
# Solo alemán tiene casos y word_order
german_cases = GrammarUnit.objects.filter(
    target_language='de',
    grammatical_category__in=['case_system', 'declension', 'word_order']
)

# Solo francés tiene verb_mood específico
french_moods = GrammarUnit.objects.filter(
    target_language='fr',
    grammatical_category='verb_mood'
)
```

---

## 📚 Recursos de Referencia

### Niveles CEFR por Idioma
- [CEFR English](https://www.cambridgeenglish.org/exams-and-tests/cefr/)
- [CEFR French - Alliance Française](https://www.alliancefr.org/cours/cours-de-francais/niveaux-de-francais)
- [CEFR German - Goethe Institut](https://www.goethe.de/en/spr/kup/prf.html)

### Documentos Internos
- `apps/grammar/models.py` - Modelo principal
- `.gemini/antigravity/brain/*/multi_language_grammar_analysis.md`
- `.gemini/antigravity/brain/*/word_order_syntax_guide.md`
- `.gemini/antigravity/brain/*/walkthrough.md`

---

## ❓ Preguntas Frecuentes

### ¿Necesito crear nueva migración al agregar idiomas?
**No.** El campo `target_language` ya existe con choices para `en`, `de`, `fr`. Solo necesitas crear los seed scripts.

### ¿Puedo usar el mismo slug en diferentes idiomas?
**Sí.** El constraint `unique_together = [['slug', 'target_language']]` lo permite.

### ¿Qué hago si mi idioma necesita una categoría nueva?
1. Agregar la categoría a `CATEGORY_CHOICES` en `models.py`
2. Crear migración con `python manage.py makemigrations`
3. Aplicar con `python manage.py migrate`
4. Documentar en este archivo

### ¿Orden de introducción pedagógica es igual entre idiomas?
**No necesariamente.** Por ejemplo:
- Inglés A1: Verb TO BE → Present Simple → A/An
- Alemán A1: Género Gramatical → Verb SEIN → Artículos (el género es crítico temprano)

Ajusta `pedagogical_sequence` según las necesidades pedagógicas del idioma específico.

---

## 🚀 Próximos Pasos

### Inmediatos
1. Crear `seed_grammar_a1_fr.py` para francés
2. Crear `seed_grammar_a1_de.py` para alemán
3. Validar que ambos funcionan correctamente

### Mediano Plazo
1. Crear grammar units A2-B1 para inglés
2. Replicar A2-B1 para francés/alemán
3. Integrar con sistema de milestones

### Largo Plazo
1. Agregar más idiomas (italiano, portugués, etc.)
2. Sistema de recomendación de grammar según errores del usuario
3. Ejercicios automáticos basados en `structural_metadata`

---

## 📝 Historial de Cambios

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2026-01-16 | Creación del documento | Sistema |
| 2026-01-16 | Implementación multi-idioma en modelo | Sistema |

---

## 💡 Notas Importantes

> [!WARNING]
> **Alemán requiere atención especial al orden de palabras.** Siempre incluir información de V2/SOV en `structural_metadata` para estructuras con verbos.

> [!IMPORTANT]
> **El género gramatical debe introducirse MUY temprano en alemán y francés** (A1.1 o A1.2), ya que afecta artículos, adjetivos, pronombres, etc.

> [!TIP]
> Consulta `structural_metadata` de grammar units ingleses existentes como referencia de formato y estructura.
