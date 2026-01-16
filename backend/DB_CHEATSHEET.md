# CHEAT SHEET - Relaciones DB YoPuedo360

## 📋 Tabla Rápida de Conexiones

```
PREGUNTA: ¿Dónde se usa "coffee"?
RESPUESTA: 
  coffee = Vocabulary.objects.get(word='coffee')
  coffee.milestone_usages.all()  ← VocabularyInMilestone
  
PREGUNTA: ¿Qué vocabulario tiene milestone "Order food"?
RESPUESTA:
  milestone = Milestone.objects.get(name='Order food')
  milestone.vocabulary_items.all()  ← VocabularyInMilestone
  
PREGUNTA: ¿En cuántos milestones se usa "can"?
RESPUESTA:
  can = GrammarUnit.objects.get(slug='can-infinitive')
  can.milestone_usages.count()  ← GrammarInMilestone
```

## 🔗 Mapa Mental

```
Scenario (Restaurant)
  └─ Milestone (Order food)
      ├─ Grammar: can+infinitive (order=1) "Can I have...?"
      └─ Vocabulary: coffee (order=3) "Can I have coffee?"

User (Juan)
  ├─ Progress: coffee → mastered
  └─ Progress: can → learning
```

## 🎯 Foreign Keys (FKs)

| Tabla | Campo FK | Apunta a | Reverse name |
|-------|----------|----------|--------------|
| Milestone | `scenario_id` | Scenario | `milestones` |
| VocabularyInMilestone | `vocabulary_id` | Vocabulary | `milestone_usages` |
| VocabularyInMilestone | `milestone_id` | Milestone | `vocabulary_items` |
| GrammarInMilestone | `grammar_id` | GrammarUnit | `milestone_usages` |
| GrammarInMilestone | `milestone_id` | Milestone | `grammar_items` |
| UserVocabularyProgress | `user_id` | User | `vocabularyprogress` |
| UserVocabularyProgress | `vocabulary_id` | Vocabulary | `user_progress` |

## 💡 Tip: Cómo Recordar

**Regla 1:** Si tabla tiene `xxx_id` → FK a tabla `Xxx`
**Regla 2:** Nombre `related_name` → cómo acceder en reversa

Ejemplo:
```python
class VocabularyInMilestone:
    vocabulary = FK(Vocabulary, related_name='milestone_usages')
    #                                        ↑
    # Acceso: coffee.milestone_usages.all()
```

## 🚀 Comandos Django Shell

```python
# Explorar
python manage.py shell

# Ver estructura
Vocabulary._meta.get_fields()

# Ver FKs
[f for f in Vocabulary._meta.get_fields() if f.many_to_one]

# Contar relaciones
coffee.milestone_usages.count()
```
