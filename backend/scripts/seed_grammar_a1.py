"""
Seed A1 Grammar Units
Compatible with 4-layer architecture
Run with: python scripts/seed_grammar_a1.py (from backend folder)
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
django.setup()

from apps.grammar.models import GrammarUnit

print("📚 Seeding A1 Grammar Units...")

# ============================================
# A1 GRAMMAR UNITS (11 unidades básicas)
# ============================================

A1_GRAMMAR = [
    {
        'slug': 'verb-to-be',
        'name': 'Verb TO BE',
        'level': 'A1',
        'grammatical_category': 'auxiliary',
        'form': 'Subject + am/is/are + complement',
        'meaning_en': 'Identity, description, states',
        'meaning_es': 'Identidad, descripción, estados',
        'pedagogical_sequence': 1,
        'examples': [
            {"en": "I am a student", "es": "Soy estudiante"},
            {"en": "She is happy", "es": "Ella está feliz"},
            {"en": "They are from Mexico", "es": "Ellos son de México"}
        ],
        'structural_metadata': {
            "pattern": "SUBJECT + am/is/are + COMPLEMENT",
            "conjugation": {
                "I": "am",
                "you": "are",
                "he/she/it": "is",
                "we": "are",
                "they": "are"
            }
        },
        'common_error_patterns': [
            {
                "error": "I is happy",
                "rule": "Use 'am' with 'I'",
                "correction": "I am happy"
            }
        ]
    },
    
    {
        'slug': 'present-simple',
        'name': 'Present Simple',
        'level': 'A1',
        'grammatical_category': 'tense',
        'form': 'Subject + verb (+ s/es for he/she/it)',
        'meaning_en': 'Routines, habits, general truths',
        'meaning_es': 'Rutinas, hábitos, verdades generales',
        'pedagogical_sequence': 2,
        'examples': [
            {"en": "I work every day", "es": "Trabajo todos los días"},
            {"en": "She speaks English", "es": "Ella habla inglés"},
            {"en": "They live in Madrid", "es": "Viven en Madrid"}
        ],
        'structural_metadata': {
            "pattern": "SUBJECT + VERB(-s)",
            "third_person_rule": "Add -s for he/she/it",
            "special_endings": {
                "s/ss/sh/ch/x/o": "-es (watches, goes)",
                "consonant+y": "-ies (studies)"
            }
        },
        'common_error_patterns': [
            {
                "error": "He work here",
                "rule": "Add -s for third person singular",
                "correction": "He works here"
            }
        ]
    },
    
    {
        'slug': 'a-an-articles',
        'name': 'A/An Articles',
        'level': 'A1',
        'grammatical_category': 'article',
        'form': 'a + consonant sound, an + vowel sound',
        'meaning_en': 'Indefinite articles (one, any)',
        'meaning_es': 'Artículos indefinidos (un, una)',
        'pedagogical_sequence': 3,
        'examples': [
            {"en": "a book", "es": "un libro"},
            {"en": "an apple", "es": "una manzana"},
            {"en": "a university", "es": "una universidad (sonido de consonante)"}
        ],
        'structural_metadata': {
            "pattern": "a/an + SINGULAR_NOUN",
            "rule": "Use 'a' before consonant SOUNDS, 'an' before vowel SOUNDS",
            "tricky_words": ["a university (yoo)", "an hour (our)"]
        }
    },
    
    {
        'slug': 'can-infinitive',
        'name': 'Can + Infinitive',
        'level': 'A1',
        'grammatical_category': 'modal_verb',
        'form': 'Subject + can/can\'t + base verb',
        'meaning_en': 'Ability, permission, possibility',
        'meaning_es': 'Habilidad, permiso, posibilidad',
        'pedagogical_sequence': 4,
        'examples': [
            {"en": "I can swim", "es": "Puedo nadar"},
            {"en": "She can't drive", "es": "Ella no puede conducir"},
            {"en": "Can you help me?", "es": "¿Puedes ayudarme?"}
        ],
        'structural_metadata': {
            "pattern": "SUBJECT + can + BASE_VERB",
            "negative": "can't / cannot",
            "question": "Can + SUBJECT + VERB?",
            "no_conjugation": "Same form for all subjects (no -s)"
        },
        'common_error_patterns': [
            {
                "error": "I can to swim",
                "rule": "No 'to' after 'can'",
                "correction": "I can swim"
            },
            {
                "error": "He cans swim",
                "rule": "No -s in modal verbs",
                "correction": "He can swim"
            }
        ]
    },
    
    {
        'slug': 'possessive-adjectives',
        'name': 'Possessive Adjectives',
        'level': 'A1',
        'grammatical_category': 'possessive',
        'form': 'Possessive + noun',
        'meaning_en': 'Ownership, belonging',
        'meaning_es': 'Pertenencia, posesión',
        'pedagogical_sequence': 5,
        'examples': [
            {"en": "my book", "es": "mi libro"},
            {"en": "her car", "es": "su coche (de ella)"},
            {"en": "their house", "es": "su casa (de ellos)"}
        ],
        'structural_metadata': {
            "pattern": "POSSESSIVE + NOUN",
            "forms": {
                "I": "my",
                "you": "your",
                "he": "his",
                "she": "her",
                "it": "its",
                "we": "our",
                "they": "their"
            }
        }
    },
    
    {
        'slug': 'there-is-are',
        'name': 'There is / There are',
        'level': 'A1',
        'grammatical_category': 'auxiliary',
        'form': 'There is + singular / There are + plural',
        'meaning_en': 'Existence, location',
        'meaning_es': 'Existencia, ubicación (hay)',
        'pedagogical_sequence': 6,
        'examples': [
            {"en": "There is a book", "es": "Hay un libro"},
            {"en": "There are three cats", "es": "Hay tres gatos"}
        ],
        'structural_metadata': {
            "pattern": "There is/are + NOUN/SUBJECT",
            "singular": "There is + singular/uncountable",
            "plural": "There are + plural",
            "negative": "There isn't / There aren't",
            "question": "Is there...? / Are there...?"
        }
    },
    
    {
        'slug': 'demonstratives',
        'name': 'This / That / These / Those',
        'level': 'A1',
        'grammatical_category': 'pronoun',
        'form': 'this/that + singular, these/those + plural',
        'meaning_en': 'Pointing, showing',
        'meaning_es': 'Señalar, demostrar',
        'pedagogical_sequence': 7,
        'examples': [
            {"en": "This is my phone", "es": "Este es mi teléfono"},
            {"en": "Those are nice", "es": "Esos son bonitos"}
        ],
        'structural_metadata': {
            "near_singular": "this",
            "near_plural": "these",
            "far_singular": "that",
            "far_plural": "those"
        }
    },
    
    {
        'slug': 'prepositions-place',
        'name': 'Prepositions of Place',
        'level': 'A1',
        'grammatical_category': 'preposition',
        'form': 'in/on/at + location',
        'meaning_en': 'Location, position',
        'meaning_es': 'Ubicación, posición',
        'pedagogical_sequence': 8,
        'examples': [
            {"en": "in the box", "es": "en la caja"},
            {"en": "on the table", "es": "sobre la mesa"},
            {"en": "at home", "es": "en casa"}
        ],
        'structural_metadata': {
            "in": "inside, enclosed spaces (in the room, in Madrid)",
            "on": "surface contact (on the table, on the wall)",
            "at": "specific point/location (at home, at the station)"
        }
    },
    
    {
        'slug': 'question-words',
        'name': 'Question Words (What, Where, When, etc.)',
        'level': 'A1',
        'grammatical_category': 'question_form',
        'form': 'Question word + auxiliary + subject + verb?',
        'meaning_en': 'Asking for information',
        'meaning_es': 'Preguntar por información',
        'pedagogical_sequence': 9,
        'examples': [
            {"en": "What is your name?", "es": "¿Cuál es tu nombre?"},
            {"en": "Where do you live?", "es": "¿Dónde vives?"},
            {"en": "When is the party?", "es": "¿Cuándo es la fiesta?"}
        ],
        'structural_metadata': {
            "what": "qué/cuál",
            "where": "dónde",
            "when": "cuándo",
            "who": "quién",
            "why": "por qué",
            "how": "cómo"
        }
    },
    
    {
        'slug': 'imperatives',
        'name': 'Imperatives',
        'level': 'A1',
        'grammatical_category': 'tense',
        'form': 'Base verb (+ complement)',
        'meaning_en': 'Commands, instructions, requests',
        'meaning_es': 'Órdenes, instrucciones, peticiones',
        'pedagogical_sequence': 10,
        'examples': [
            {"en": "Open the door", "es": "Abre la puerta"},
            {"en": "Don't run", "es": "No corras"},
            {"en": "Please sit down", "es": "Por favor siéntate"}
        ],
        'structural_metadata': {
            "pattern": "VERB (+ complement)",
            "negative": "Don't + VERB",
            "polite": "Please + VERB / VERB + please"
        }
    },
    
    {
        'slug': 'plural-nouns',
        'name': 'Plural Nouns',
        'level': 'A1',
        'grammatical_category': 'article',
        'form': 'noun + s/es/ies',
        'meaning_en': 'More than one',
        'meaning_es': 'Más de uno',
        'pedagogical_sequence': 11,
        'examples': [
            {"en": "cat → cats", "es": "gato → gatos"},
            {"en": "box → boxes", "es": "caja → cajas"},
            {"en": "baby → babies", "es": "bebé → bebés"}
        ],
        'structural_metadata': {
            "regular": "Add -s (books, cats)",
            "s_sh_ch_x": "Add -es (boxes, watches)",
            "consonant_y": "Change y to -ies (baby → babies)",
            "irregular": ["man→men", "child→children", "person→people"]
        }
    },
    
    {
        'slug': 'adverbs-frequency',
        'name': 'Adverbs of Frequency',
        'level': 'A1',
        'grammatical_category': 'adverb',
        'form': 'Subject + adverb + verb / Subject + be + adverb',
        'meaning_en': 'How often something happens',
        'meaning_es': 'Qué tan seguido ocurre algo',
        'pedagogical_sequence': 12,
        'examples': [
            {"en": "I always drink coffee", "es": "Siempre tomo café"},
            {"en": "She usually works late", "es": "Ella usualmente trabaja tarde"},
            {"en": "They are never late", "es": "Nunca llegan tarde"}
        ],
        'structural_metadata': {
            "pattern": "SUBJECT + ADVERB + VERB / SUBJECT + BE + ADVERB",
            "frequency_scale": {
                "always": "100% - siempre",
                "usually": "80% - usualmente",
                "often": "60% - a menudo",
                "sometimes": "40% - a veces",
                "rarely": "20% - raramente",
                "never": "0% - nunca"
            },
            "position_with_be": "After BE verb (I am always happy)",
            "position_with_other_verbs": "Before main verb (I always eat breakfast)"
        },
        'common_error_patterns': [
            {
                "error": "I eat always breakfast",
                "rule": "Adverb goes before main verb",
                "correction": "I always eat breakfast"
            },
            {
                "error": "She always is late",
                "rule": "Adverb goes after BE verb",
                "correction": "She is always late"
            }
        ]
    },
    
    {
        'slug': 'like-love-hate-noun',
        'name': 'Like / Love / Hate + Noun',
        'level': 'A1',
        'grammatical_category': 'verb',
        'form': 'Subject + like/love/hate + noun',
        'meaning_en': 'Express preferences and feelings',
        'meaning_es': 'Expresar preferencias y sentimientos',
        'pedagogical_sequence': 13,
        'examples': [
            {"en": "I like pizza", "es": "Me gusta la pizza"},
            {"en": "She loves music", "es": "Ella ama la música"},
            {"en": "They hate cold weather", "es": "Ellos odian el clima frío"}
        ],
        'structural_metadata': {
            "pattern": "SUBJECT + like/love/hate + NOUN",
            "conjugation": {
                "I/you/we/they": "like/love/hate",
                "he/she/it": "likes/loves/hates"
            },
            "intensity": {
                "love": "very positive",
                "like": "positive",
                "hate": "very negative"
            },
            "also_with_gerund": "Can also use -ing form (I like swimming)"
        },
        'common_error_patterns': [
            {
                "error": "He like pizza",
                "rule": "Add -s for third person singular",
                "correction": "He likes pizza"
            }
        ]
    },
    
    {
        'slug': 'simple-adjectives',
        'name': 'Simple Adjectives',
        'level': 'A1',
        'grammatical_category': 'adjective',
        'form': 'adjective + noun / be + adjective',
        'meaning_en': 'Describe qualities and characteristics',
        'meaning_es': 'Describir cualidades y características',
        'pedagogical_sequence': 14,
        'examples': [
            {"en": "a big house", "es": "una casa grande"},
            {"en": "The car is small", "es": "El carro es pequeño"},
            {"en": "good food", "es": "comida buena"},
            {"en": "It's bad weather", "es": "Es mal clima"}
        ],
        'structural_metadata': {
            "pattern": "ADJ + NOUN / BE + ADJECTIVE",
            "basic_adjectives": {
                "size": ["big", "small", "large", "little"],
                "quality": ["good", "bad", "nice", "beautiful"],
                "age": ["new", "old", "young"],
                "color": ["red", "blue", "green", "yellow"],
                "feeling": ["happy", "sad", "tired", "hungry"]
            },
            "position": "Before noun OR after BE verb",
            "no_agreement": "Adjectives don't change form (unlike Spanish)"
        },
        'common_error_patterns': [
            {
                "error": "a house big",
                "rule": "Adjective comes before noun in English",
                "correction": "a big house"
            },
            {
                "error": "bigs houses",
                "rule": "Adjectives don't have plural form",
                "correction": "big houses"
            }
        ]
    },
    
    {
        'slug': 'conjunction-and',
        'name': 'Conjunction: And',
        'level': 'A1',
        'grammatical_category': 'conjunction',
        'form': 'word/phrase + and + word/phrase',
        'meaning_en': 'Connect similar ideas, add information',
        'meaning_es': 'Conectar ideas similares, agregar información',
        'pedagogical_sequence': 15,
        'examples': [
            {"en": "I like coffee and tea", "es": "Me gusta el café y el té"},
            {"en": "She is smart and kind", "es": "Ella es inteligente y amable"},
            {"en": "We work and study", "es": "Trabajamos y estudiamos"}
        ],
        'structural_metadata': {
            "pattern": "ITEM1 + and + ITEM2",
            "usage": "Connect nouns, adjectives, verbs, or sentences",
            "meaning": "Addition, combination",
            "examples_types": {
                "nouns": "bread and butter",
                "adjectives": "happy and healthy",
                "verbs": "read and write",
                "sentences": "I like pizza and my brother likes pasta"
            }
        }
    },
    
    {
        'slug': 'conjunction-but',
        'name': 'Conjunction: But',
        'level': 'A1',
        'grammatical_category': 'conjunction',
        'form': 'sentence + but + contrasting sentence',
        'meaning_en': 'Show contrast or opposition',
        'meaning_es': 'Mostrar contraste u oposición',
        'pedagogical_sequence': 16,
        'examples': [
            {"en": "I like coffee but I don't like tea", "es": "Me gusta el café pero no me gusta el té"},
            {"en": "She is small but strong", "es": "Ella es pequeña pero fuerte"},
            {"en": "It's expensive but good", "es": "Es caro pero bueno"}
        ],
        'structural_metadata': {
            "pattern": "STATEMENT1 + but + CONTRASTING_STATEMENT2",
            "usage": "Connect contrasting ideas",
            "meaning": "Contrast, opposition, exception",
            "difference_from_and": "'and' adds similar ideas, 'but' shows contrast",
            "examples_types": {
                "adjectives": "big but light",
                "sentences": "I'm tired but happy",
                "preferences": "I like it but she doesn't"
            }
        },
        'common_error_patterns': [
            {
                "error": "I like coffee but also tea",
                "rule": "'but' is for contrast, use 'and' for addition",
                "correction": "I like coffee and tea"
            }
        ]
    },
]

# Create grammar units
created_count = 0
updated_count = 0

for data in A1_GRAMMAR:
    grammar, created = GrammarUnit.objects.update_or_create(
        slug=data['slug'],
        target_language='en',  # English grammar units
        defaults={
            'name': data['name'],
            'level': data['level'],
            'grammatical_category': data['grammatical_category'],
            'form': data['form'],
            'meaning_en': data['meaning_en'],
            'meaning_es': data['meaning_es'],
            'pedagogical_sequence': data['pedagogical_sequence'],
            'examples': data.get('examples', []),
            'structural_metadata': data.get('structural_metadata', {}),
            'common_error_patterns': data.get('common_error_patterns', []),
            'is_universal': True,
            'source': 'manual',
        }
    )
    
    if created:
        created_count += 1
        print(f"  ✅ Created: {grammar}")
    else:
        updated_count += 1
        print(f"  🔄 Updated: {grammar}")

print(f"\n📊 Summary:")
print(f"  ✅ Created: {created_count}")
print(f"  🔄 Updated: {updated_count}")
print(f"  📚 Total A1 Grammar Units: {GrammarUnit.objects.filter(level='A1').count()}")
print("\n✅ A1 Grammar seeded successfully!")
