"""
Seed A2 Grammar Units
Compatible with 4-layer architecture
Run with: python scripts/seed_grammar_a2.py (from backend folder)
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
django.setup()

from apps.grammar.models import GrammarUnit

print("📚 Seeding A2 Grammar Units...")

# ============================================
# A2 GRAMMAR UNITS (20 unidades intermedias)
# ============================================

A2_GRAMMAR = [
    {
        'slug': 'past-simple',
        'name': 'Past Simple',
        'level': 'A2',
        'grammatical_category': 'tense',
        'form': 'Subject + verb-ed / irregular past',
        'meaning_en': 'Completed actions in the past',
        'meaning_es': 'Acciones completadas en el pasado',
        'pedagogical_sequence': 17,
        'examples': [
            {"en": "I worked yesterday", "es": "Trabajé ayer"},
            {"en": "She went to the store", "es": "Ella fue a la tienda"},
            {"en": "They played football", "es": "Jugaron fútbol"}
        ],
        'structural_metadata': {
            "pattern": "SUBJECT + VERB-ed/irregular",
            "regular_ending": "-ed",
            "irregular_examples": {
                "go": "went",
                "eat": "ate",
                "see": "saw"
            }
        },
        'common_error_patterns': [
            {
                "error": "I goed to school",
                "rule": "Use irregular past form 'went'",
                "correction": "I went to school"
            }
        ]
    },
    
    {
        'slug': 'present-continuous',
        'name': 'Present Continuous',
        'level': 'A2',
        'grammatical_category': 'tense',
        'form': 'Subject + am/is/are + verb-ing',
        'meaning_en': 'Actions happening now',
        'meaning_es': 'Acciones ocurriendo ahora',
        'pedagogical_sequence': 18,
        'examples': [
            {"en": "I am working now", "es": "Estoy trabajando ahora"},
            {"en": "She is eating lunch", "es": "Ella está comiendo"},
            {"en": "They are studying", "es": "Están estudiando"}
        ],
        'structural_metadata': {
            "pattern": "SUBJECT + be + VERB-ing",
            "spelling_rules": {
                "double_consonant": "sit → sitting",
                "drop_e": "make → making",
                "ie_to_y": "lie → lying"
            }
        },
        'common_error_patterns': [
            {
                "error": "I working now",
                "rule": "Need 'am/is/are' before -ing",
                "correction": "I am working now"
            }
        ]
    },
    
    {
        'slug': 'going-to-future',
        'name': 'Going to (Future)',
        'level': 'A2',
        'grammatical_category': 'tense',
        'form': 'Subject + am/is/are going to + verb',
        'meaning_en': 'Future plans and intentions',
        'meaning_es': 'Planes e intenciones futuras',
        'pedagogical_sequence': 19,
        'examples': [
            {"en": "I am going to study tonight", "es": "Voy a estudiar esta noche"},
            {"en": "She is going to travel tomorrow", "es": "Ella va a viajar mañana"},
            {"en": "They are going to visit us", "es": "Van a visitarnos"}
        ],
        'structural_metadata': {
            "pattern": "SUBJECT + be + going to + VERB",
            "vs_will": "going to = planned, will = spontaneous"
        },
        'common_error_patterns': [
            {
                "error": "I going to study",
                "rule": "Need 'am/is/are' before 'going to'",
                "correction": "I am going to study"
            }
        ]
    },
    
    {
        'slug': 'comparatives',
        'name': 'Comparative Adjectives',
        'level': 'A2',
        'grammatical_category': 'adjective',
        'form': '-er / more + adjective + than',
        'meaning_en': 'Compare two things',
        'meaning_es': 'Comparar dos cosas',
        'pedagogical_sequence': 20,
        'examples': [
            {"en": "She is taller than me", "es": "Ella es más alta que yo"},
            {"en": "This is more expensive", "es": "Esto es más caro"},
            {"en": "He runs faster than John", "es": "Él corre más rápido que John"}
        ],
        'structural_metadata': {
            "pattern_short": "ADJ-er + than",
            "pattern_long": "more + ADJ + than",
            "rules": {
                "1_syllable": "add -er (tall → taller)",
                "2_syllables_y": "add -er (happy → happier)",
                "2+_syllables": "use more (expensive → more expensive)"
            },
            "irregular": {
                "good": "better",
                "bad": "worse",
                "far": "farther/further"
            }
        },
        'common_error_patterns': [
            {
                "error": "more tall than",
                "rule": "Use -er for short adjectives",
                "correction": "taller than"
            }
        ]
    },
    
    {
        'slug': 'superlatives',
        'name': 'Superlative Adjectives',
        'level': 'A2',
        'grammatical_category': 'adjective',
        'form': 'the + -est / most + adjective',
        'meaning_en': 'The most/least of a group',
        'meaning_es': 'El más/menos de un grupo',
        'pedagogical_sequence': 21,
        'examples': [
            {"en": "She is the tallest in class", "es": "Ella es la más alta de la clase"},
            {"en": "This is the most expensive", "es": "Este es el más caro"},
            {"en": "He is the best player", "es": "Él es el mejor jugador"}
        ],
        'structural_metadata': {
            "pattern_short": "the + ADJ-est",
            "pattern_long": "the most + ADJ",
            "irregular": {
                "good": "the best",
                "bad": "the worst",
                "far": "the farthest"
            }
        },
        'common_error_patterns': [
            {
                "error": "the most tall",
                "rule": "Use -est for short adjectives",
                "correction": "the tallest"
            }
        ]
    },
    
    {
        'slug': 'adverbs-of-manner',
        'name': 'Adverbs of Manner',
        'level': 'A2',
        'grammatical_category': 'adverb',
        'form': 'adjective + -ly',
        'meaning_en': 'How an action is done',
        'meaning_es': 'Cómo se hace una acción',
        'pedagogical_sequence': 22,
        'examples': [
            {"en": "She speaks slowly", "es": "Ella habla lentamente"},
            {"en": "He drives carefully", "es": "Él maneja cuidadosamente"},
            {"en": "They work quickly", "es": "Trabajan rápidamente"}
        ],
        'structural_metadata': {
            "pattern": "ADJ + -ly = ADV",
            "placement": "usually after verb",
            "irregular": {
                "good": "well",
                "fast": "fast",
                "hard": "hard"
            }
        },
        'common_error_patterns': [
            {
                "error": "She speaks good",
                "rule": "Use adverb 'well' not adjective 'good'",
                "correction": "She speaks well"
            }
        ]
    },
    
    {
        'slug': 'countable-uncountable',
        'name': 'Countable / Uncountable Nouns',
        'level': 'A2',
        'grammatical_category': 'noun',
        'form': 'some/any/much/many with nouns',
        'meaning_en': 'Nouns you can/cannot count',
        'meaning_es': 'Sustantivos contables/incontables',
        'pedagogical_sequence': 23,
        'examples': [
            {"en": "I have some apples (countable)", "es": "Tengo algunas manzanas"},
            {"en": "I need some water (uncountable)", "es": "Necesito agua"},
            {"en": "How many books?", "es": "¿Cuántos libros?"},
            {"en": "How much money?", "es": "¿Cuánto dinero?"}
        ],
        'structural_metadata': {
            "countable": "many, a few, number",
            "uncountable": "much, a little, amount",
            "both": "some, any, a lot of"
        },
        'common_error_patterns': [
            {
                "error": "How many water?",
                "rule": "Use 'much' with uncountable",
                "correction": "How much water?"
            }
        ]
    },
    
    {
        'slug': 'object-pronouns',
        'name': 'Object Pronouns',
        'level': 'A2',
        'grammatical_category': 'pronoun',
        'form': 'me/you/him/her/it/us/them',
        'meaning_en': 'Pronouns receiving the action',
        'meaning_es': 'Pronombres objeto',
        'pedagogical_sequence': 24,
        'examples': [
            {"en": "She loves me", "es": "Ella me ama"},
            {"en": "I called him", "es": "Lo llamé"},
            {"en": "He gave it to us", "es": "Nos lo dio"}
        ],
        'structural_metadata': {
            "mapping": {
                "I": "me",
                "you": "you",
                "he": "him",
                "she": "her",
                "it": "it",
                "we": "us",
                "they": "them"
            },
            "placement": "after verb or preposition"
        },
        'common_error_patterns': [
            {
                "error": "She loves I",
                "rule": "Use object pronoun 'me'",
                "correction": "She loves me"
            }
        ]
    },
    
    {
        'slug': 'have-to-must',
        'name': 'Have to / Must',
        'level': 'A2',
        'grammatical_category': 'modal',
        'form': 'Subject + have to / must + verb',
        'meaning_en': 'Obligation and necessity',
        'meaning_es': 'Obligación y necesidad',
        'pedagogical_sequence': 25,
        'examples': [
            {"en": "I have to work tomorrow", "es": "Tengo que trabajar mañana"},
            {"en": "You must be quiet", "es": "Debes estar callado"},
            {"en": "She has to study", "es": "Ella tiene que estudiar"}
        ],
        'structural_metadata': {
            "have_to": "external obligation",
            "must": "internal obligation / strong advice",
            "negative": {
                "don't have to": "not necessary",
                "must not": "prohibited"
            }
        },
        'common_error_patterns': [
            {
                "error": "I must to go",
                "rule": "'must' doesn't use 'to'",
                "correction": "I must go"
            }
        ]
    },
    
    {
        'slug': 'should-ought-to',
        'name': 'Should / Ought to',
        'level': 'A2',
        'grammatical_category': 'modal',
        'form': 'Subject + should / ought to + verb',
        'meaning_en': 'Advice and recommendations',
        'meaning_es': 'Consejos y recomendaciones',
        'pedagogical_sequence': 26,
        'examples': [
            {"en": "You should rest", "es": "Deberías descansar"},
            {"en": "We ought to leave now", "es": "Deberíamos irnos ahora"},
            {"en": "She should see a doctor", "es": "Ella debería ver un doctor"}
        ],
        'structural_metadata': {
            "pattern": "SUBJECT + should/ought to + VERB",
            "similarity": "should ≈ ought to",
            "strength": "weaker than must"
        },
        'common_error_patterns': [
            {
                "error": "You should to rest",
                "rule": "'should' doesn't use 'to'",
                "correction": "You should rest"
            }
        ]
    },
    
    {
        'slug': 'prepositions-of-time',
        'name': 'Prepositions of Time',
        'level': 'A2',
        'grammatical_category': 'preposition',
        'form': 'at/on/in with time',
        'meaning_en': 'When something happens',
        'meaning_es': 'Cuándo ocurre algo',
        'pedagogical_sequence': 27,
        'examples': [
            {"en": "at 3 o'clock", "es": "a las 3"},
            {"en": "on Monday", "es": "el lunes"},
            {"en": "in January", "es": "en enero"},
            {"en": "in the morning", "es": "por la mañana"}
        ],
        'structural_metadata': {
            "at": "specific time (at 5pm, at night)",
            "on": "days and dates (on Monday, on June 1st)",
            "in": "months, years, periods (in May, in 2024, in the morning)"
        },
        'common_error_patterns': [
            {
                "error": "in Monday",
                "rule": "Use 'on' with days",
                "correction": "on Monday"
            }
        ]
    },
    
    {
        'slug': 'some-any',
        'name': 'Some / Any',
        'level': 'A2',
        'grammatical_category': 'determiner',
        'form': 'some in positive, any in negative/questions',
        'meaning_en': 'Indefinite quantity',
        'meaning_es': 'Cantidad indefinida',
        'pedagogical_sequence': 28,
        'examples': [
            {"en": "I have some money", "es": "Tengo algo de dinero"},
            {"en": "Do you have any questions?", "es": "¿Tienes alguna pregunta?"},
            {"en": "I don't have any time", "es": "No tengo tiempo"}
        ],
        'structural_metadata': {
            "some": "affirmative sentences, offers, requests",
            "any": "negative sentences, questions",
            "exceptions": "Would you like some coffee? (offer)"
        },
        'common_error_patterns': [
            {
                "error": "I have any money",
                "rule": "Use 'some' in positive",
                "correction": "I have some money"
            }
        ]
    },
    
    {
        'slug': 'too-enough',
        'name': 'Too / Enough',
        'level': 'A2',
        'grammatical_category': 'adverb',
        'form': 'too + adj, adj + enough',
        'meaning_en': 'Excessive or sufficient',
        'meaning_es': 'Excesivo o suficiente',
        'pedagogical_sequence': 29,
        'examples': [
            {"en": "It's too expensive", "es": "Es demasiado caro"},
            {"en": "I'm not tall enough", "es": "No soy lo suficientemente alto"},
            {"en": "She's old enough to drive", "es": "Tiene edad suficiente para manejar"}
        ],
        'structural_metadata': {
            "too": "before adjective (negative)",
            "enough": "after adjective (positive/neutral)",
            "pattern_too": "too + ADJ",
            "pattern_enough": "ADJ + enough"
        },
        'common_error_patterns': [
            {
                "error": "enough tall",
                "rule": "'enough' comes after adjective",
                "correction": "tall enough"
            }
        ]
    },
    
    {
        'slug': 'reflexive-pronouns',
        'name': 'Reflexive Pronouns',
        'level': 'A2',
        'grammatical_category': 'pronoun',
        'form': 'myself/yourself/himself/etc.',
        'meaning_en': 'Action done to oneself',
        'meaning_es': 'Acción hecha a uno mismo',
        'pedagogical_sequence': 30,
        'examples': [
            {"en": "I hurt myself", "es": "Me lastimé"},
            {"en": "She introduced herself", "es": "Ella se presentó"},
            {"en": "Enjoy yourself!", "es": "¡Disfruta!"}
        ],
        'structural_metadata': {
            "forms": {
                "I": "myself",
                "you": "yourself/yourselves",
                "he": "himself",
                "she": "herself",
                "it": "itself",
                "we": "ourselves",
                "they": "themselves"
            }
        },
        'common_error_patterns': [
            {
                "error": "I cut me",
                "rule": "Use reflexive 'myself'",
                "correction": "I cut myself"
            }
        ]
    },
    
    {
        'slug': 'relative-pronouns',
        'name': 'Relative Pronouns (who/which/that)',
        'level': 'A2',
        'grammatical_category': 'pronoun',
        'form': 'who/which/that + clause',
        'meaning_en': 'Connect related information',
        'meaning_es': 'Conectar información relacionada',
        'pedagogical_sequence': 31,
        'examples': [
            {"en": "The man who called", "es": "El hombre que llamó"},
            {"en": "The book which I read", "es": "El libro que leí"},
            {"en": "The car that I bought", "es": "El auto que compré"}
        ],
        'structural_metadata': {
            "who": "for people",
            "which": "for things",
            "that": "for people or things",
            "defining_clause": "essential information (no commas)"
        },
        'common_error_patterns': [
            {
                "error": "The man which called",
                "rule": "Use 'who' for people",
                "correction": "The man who called"
            }
        ]
    },
    
    {
        'slug': 'phrasal-verbs-basic',
        'name': 'Basic Phrasal Verbs',
        'level': 'A2',
        'grammatical_category': 'verb',
        'form': 'verb + particle',
        'meaning_en': 'Common verb combinations',
        'meaning_es': 'Verbos compuestos comunes',
        'pedagogical_sequence': 32,
        'examples': [
            {"en": "Turn on the light", "es": "Enciende la luz"},
            {"en": "Get up early", "es": "Levantarse temprano"},
            {"en": "Look for my keys", "es": "Buscar mis llaves"}
        ],
        'structural_metadata': {
            "common_phrasal_verbs": {
                "turn on/off": "encender/apagar",
                "get up": "levantarse",
                "look for": "buscar",
                "pick up": "recoger",
                "put on": "ponerse (ropa)"
            },
            "separable": "Turn the light on",
            "inseparable": "Look for it (not: look it for)"
        },
        'common_error_patterns': [
            {
                "error": "Open the TV",
                "rule": "Use 'turn on' for electronic devices",
                "correction": "Turn on the TV"
            }
        ]
    },
    
    {
        'slug': 'used-to',
        'name': 'Used to',
        'level': 'A2',
        'grammatical_category': 'modal',
        'form': 'Subject + used to + verb',
        'meaning_en': 'Past habits (no longer true)',
        'meaning_es': 'Hábitos pasados (ya no)',
        'pedagogical_sequence': 33,
        'examples': [
            {"en": "I used to smoke", "es": "Solía fumar"},
            {"en": "She used to live here", "es": "Ella vivía aquí"},
            {"en": "We used to play soccer", "es": "Solíamos jugar fútbol"}
        ],
        'structural_metadata': {
            "pattern": "SUBJECT + used to + VERB",
            "meaning": "past habit or state (finished)",
            "negative": "didn't use to",
            "question": "Did you use to...?"
        },
        'common_error_patterns': [
            {
                "error": "I use to smoke",
                "rule": "Past form is 'used to'",
                "correction": "I used to smoke"
            }
        ]
    },
    
    {
        'slug': 'question-tags',
        'name': 'Question Tags',
        'level': 'A2',
        'grammatical_category': 'question',
        'form': 'Statement + tag',
        'meaning_en': 'Confirm or check information',
        'meaning_es': 'Confirmar o verificar información',
        'pedagogical_sequence': 34,
        'examples': [
            {"en": "You like coffee, don't you?", "es": "Te gusta el café, ¿verdad?"},
            {"en": "She isn't here, is she?", "es": "Ella no está aquí, ¿verdad?"},
            {"en": "They came yesterday, didn't they?", "es": "Vinieron ayer, ¿verdad?"}
        ],
        'structural_metadata': {
            "rule": "positive statement → negative tag",
            "rule2": "negative statement → positive tag",
            "pattern": "STATEMENT, AUXILIARY + PRONOUN?"
        },
        'common_error_patterns': [
            {
                "error": "You like coffee, do you?",
                "rule": "Positive statement needs negative tag",
                "correction": "You like coffee, don't you?"
            }
        ]
    },
    
    {
        'slug': 'present-perfect-introduction',
        'name': 'Present Perfect (Introduction)',
        'level': 'A2',
        'grammatical_category': 'tense',
        'form': 'Subject + have/has + past participle',
        'meaning_en': 'Past actions with present relevance',
        'meaning_es': 'Acciones pasadas con relevancia presente',
        'pedagogical_sequence': 35,
        'examples': [
            {"en": "I have visited Paris", "es": "He visitado París"},
            {"en": "She has finished her work", "es": "Ella ha terminado su trabajo"},
            {"en": "They have lived here for 5 years", "es": "Han vivido aquí por 5 años"}
        ],
        'structural_metadata': {
            "pattern": "SUBJECT + have/has + PAST PARTICIPLE",
            "uses": ["experience", "change", "unfinished time"],
            "vs_past_simple": "Present perfect = no specific time"
        },
        'common_error_patterns': [
            {
                "error": "I have visited Paris yesterday",
                "rule": "Don't use with specific past time",
                "correction": "I visited Paris yesterday"
            }
        ]
    },
    
    {
        'slug': 'both-either-neither',
        'name': 'Both / Either / Neither',
        'level': 'A2',
        'grammatical_category': 'determiner',
        'form': 'both/either/neither + noun',
        'meaning_en': 'Refer to two things',
        'meaning_es': 'Referirse a dos cosas',
        'pedagogical_sequence': 36,
        'examples': [
            {"en": "Both options are good", "es": "Ambas opciones son buenas"},
            {"en": "Either choice is fine", "es": "Cualquiera de las dos opciones está bien"},
            {"en": "Neither answer is correct", "es": "Ninguna respuesta es correcta"}
        ],
        'structural_metadata': {
            "both": "two things together (positive)",
            "either": "one OR the other",
            "neither": "NOT one and NOT the other (negative)"
        },
        'common_error_patterns': [
            {
                "error": "Neither options is good",
                "rule": "'neither' takes singular verb",
                "correction": "Neither option is good"
            }
        ]
    },
]

# ============================================
# SAVE TO DATABASE
# ============================================

created = 0
updated = 0

for grammar_data in A2_GRAMMAR:
    obj, created_flag = GrammarUnit.objects.update_or_create(
        slug=grammar_data['slug'],
        defaults=grammar_data
    )
    
    if created_flag:
        created += 1
        print(f"  ✅ Created: {grammar_data['name']}")
    else:
        updated += 1
        print(f"  🔄 Updated: {grammar_data['name']}")

print(f"\n✅ Seeding complete!")
print(f"   Created: {created}")
print(f"   Updated: {updated}")
print(f"   Total A2 Grammar Units: {GrammarUnit.objects.filter(level='A2').count()}")
