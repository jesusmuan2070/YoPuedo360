"""
Seed A1 Grammar Topics
Run with: python scripts/seed_grammar_a1.py (from backend folder)
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
django.setup()

from apps.content.models import GrammarTopic, GrammarLesson

print("📚 Seeding A1 Grammar Topics...")

# ============================================
# A1 GRAMMAR TOPICS (11 topics obligatorios)
# ============================================

A1_GRAMMAR = [
    {
        'slug': 'a1-verb-to-be',
        'name': 'Verb TO BE',
        'name_es': 'Verbo TO BE (ser/estar)',
        'order': 1,
        'description': 'El verbo más importante en inglés. Se usa para identificar, describir y expresar estados.',
        'pattern': 'Subject + am/is/are + complement',
        'examples': [
            "I am a student",
            "She is happy", 
            "They are from Mexico",
            "It is cold today"
        ],
        'rules': [
            "I → am",
            "He/She/It → is",
            "You/We/They → are"
        ],
        'lessons': [
            ('Affirmative', "I am, You are, He is...", ["I am happy", "She is tall"]),
            ('Negative', "Add 'not' after the verb", ["I am not tired", "He is not here"]),
            ('Questions', "Invert subject and verb", ["Are you ready?", "Is she your sister?"]),
            ('Short answers', "Yes, I am / No, I'm not", ["Yes, she is", "No, they aren't"]),
        ]
    },
    {
        'slug': 'a1-present-simple',
        'name': 'Present Simple',
        'name_es': 'Presente Simple',
        'order': 2,
        'description': 'Para hablar de rutinas, hábitos y verdades generales.',
        'pattern': 'Subject + verb (+ s/es for he/she/it)',
        'examples': [
            "I work every day",
            "She speaks English",
            "They live in Madrid"
        ],
        'rules': [
            "Add -s for he/she/it: work → works",
            "Add -es after s, sh, ch, x: watch → watches",
            "Change y to ies: study → studies"
        ],
        'lessons': [
            ('Affirmative', "I work, She works", ["I eat breakfast at 8", "He plays football"]),
            ('Negative', "do/does + not + verb", ["I don't like coffee", "She doesn't work here"]),
            ('Questions', "Do/Does + subject + verb?", ["Do you speak Spanish?", "Does he live here?"]),
        ]
    },
    {
        'slug': 'a1-articles',
        'name': 'Articles (a, an, the)',
        'name_es': 'Artículos',
        'order': 3,
        'description': 'Palabras que van antes de sustantivos.',
        'pattern': 'a/an + singular noun, the + specific noun',
        'examples': [
            "a book, an apple, the sun",
            "I have a car",
            "The teacher is nice"
        ],
        'rules': [
            "a → before consonant sounds: a book, a university",
            "an → before vowel sounds: an apple, an hour",
            "the → specific or unique things: the moon, the president"
        ],
        'lessons': [
            ('Indefinite a/an', "Use for general things", ["I want a coffee", "She is an engineer"]),
            ('Definite the', "Use for specific things", ["The book on the table", "The sun is hot"]),
            ('No article', "With plurals and uncountable", ["I like music", "Dogs are friendly"]),
        ]
    },
    {
        'slug': 'a1-plurals',
        'name': 'Plural Nouns',
        'name_es': 'Sustantivos Plurales',
        'order': 4,
        'description': 'Cómo formar plurales en inglés.',
        'pattern': 'noun + s/es',
        'examples': [
            "cat → cats",
            "box → boxes",
            "baby → babies"
        ],
        'rules': [
            "Most nouns: add -s: book → books",
            "Nouns ending in s, x, ch, sh: add -es: bus → buses",
            "Nouns ending in consonant + y: change to -ies: city → cities",
            "Irregular: man → men, child → children, person → people"
        ],
        'lessons': [
            ('Regular plurals', "Add -s or -es", ["two cats", "three boxes"]),
            ('Irregular plurals', "Common exceptions", ["children", "people", "teeth"]),
        ]
    },
    {
        'slug': 'a1-possessives',
        'name': 'Possessive Adjectives',
        'name_es': 'Adjetivos Posesivos',
        'order': 5,
        'description': 'Palabras que indican pertenencia.',
        'pattern': 'Possessive + noun',
        'examples': [
            "my book, your car, his phone",
            "This is my house",
            "Her name is Maria"
        ],
        'rules': [
            "I → my",
            "You → your", 
            "He → his, She → her, It → its",
            "We → our, They → their"
        ],
        'lessons': [
            ('Singular possessives', "my, your, his, her, its", ["my name", "her car"]),
            ('Plural possessives', "our, their", ["our house", "their children"]),
        ]
    },
    {
        'slug': 'a1-demonstratives',
        'name': 'Demonstratives',
        'name_es': 'Demostrativos',
        'order': 6,
        'description': 'This, that, these, those - para señalar objetos.',
        'pattern': 'this/that + singular, these/those + plural',
        'examples': [
            "This is my phone",
            "That book is interesting",
            "These are my friends"
        ],
        'rules': [
            "this/these → near (aquí)",
            "that/those → far (allá)",
            "this/that → singular",
            "these/those → plural"
        ],
        'lessons': [
            ('Near: this/these', "Things close to you", ["This is delicious", "These shoes are new"]),
            ('Far: that/those', "Things far from you", ["That car is expensive", "Those people are nice"]),
        ]
    },
    {
        'slug': 'a1-there-is-are',
        'name': 'There is / There are',
        'name_es': 'Hay (singular/plural)',
        'order': 7,
        'description': 'Para decir que algo existe o está en un lugar.',
        'pattern': 'There is + singular / There are + plural',
        'examples': [
            "There is a book on the table",
            "There are three cats in the garden"
        ],
        'rules': [
            "There is → singular or uncountable: There is milk",
            "There are → plural: There are two chairs",
            "Negative: There isn't / There aren't",
            "Question: Is there...? / Are there...?"
        ],
        'lessons': [
            ('Affirmative', "There is/are", ["There is a park nearby", "There are many students"]),
            ('Negative & Questions', "There isn't, Is there?", ["Is there a bathroom?", "There aren't any problems"]),
        ]
    },
    {
        'slug': 'a1-can-cant',
        'name': 'Can / Can\'t',
        'name_es': 'Poder / No poder',
        'order': 8,
        'description': 'Para hablar de habilidades y permisos.',
        'pattern': 'Subject + can/can\'t + verb (base form)',
        'examples': [
            "I can swim",
            "She can't drive",
            "Can you help me?"
        ],
        'rules': [
            "Can is the same for all subjects (no 's')",
            "Can't = cannot (negative)",
            "Can + verb (no 'to'): I can swim (NOT: I can to swim)"
        ],
        'lessons': [
            ('Ability', "Talk about skills", ["I can play guitar", "She can speak French"]),
            ('Permission & Requests', "Ask for permission", ["Can I use your phone?", "Can you open the door?"]),
        ]
    },
    {
        'slug': 'a1-basic-questions',
        'name': 'Question Words',
        'name_es': 'Palabras interrogativas',
        'order': 9,
        'description': 'What, Where, When, Who, Why, How.',
        'pattern': 'Question word + auxiliary + subject + verb?',
        'examples': [
            "What is your name?",
            "Where do you live?",
            "How are you?"
        ],
        'rules': [
            "What = Qué",
            "Where = Dónde",
            "When = Cuándo",
            "Who = Quién",
            "Why = Por qué",
            "How = Cómo"
        ],
        'lessons': [
            ('What & Where', "Things and places", ["What is this?", "Where is the bathroom?"]),
            ('Who & When', "People and time", ["Who is she?", "When is the party?"]),
            ('Why & How', "Reasons and manner", ["Why are you sad?", "How do you do it?"]),
        ]
    },
    {
        'slug': 'a1-imperatives',
        'name': 'Imperatives',
        'name_es': 'Imperativos',
        'order': 10,
        'description': 'Dar órdenes, instrucciones y consejos.',
        'pattern': 'Verb (base form) + complement',
        'examples': [
            "Open the door",
            "Sit down, please",
            "Don't touch that!"
        ],
        'rules': [
            "No subject needed",
            "Use base form of verb",
            "Negative: Don't + verb",
            "Add 'please' to be polite"
        ],
        'lessons': [
            ('Affirmative commands', "Do something", ["Come here", "Listen carefully"]),
            ('Negative commands', "Don't do something", ["Don't run", "Don't be late"]),
        ]
    },
    {
        'slug': 'a1-prepositions-place',
        'name': 'Prepositions of Place',
        'name_es': 'Preposiciones de lugar',
        'order': 11,
        'description': 'In, on, at, under, next to, between.',
        'pattern': 'noun/pronoun + preposition + place',
        'examples': [
            "The book is on the table",
            "She lives in Madrid",
            "I'm at the office"
        ],
        'rules': [
            "in → inside: in the box, in the city",
            "on → surface: on the table, on the wall",
            "at → specific point: at home, at work, at the station"
        ],
        'lessons': [
            ('In, On, At', "Basic positions", ["in the room", "on the desk", "at school"]),
            ('Other prepositions', "Under, next to, between", ["under the bed", "next to me", "between us"]),
        ]
    },
]

# Create topics and lessons
for data in A1_GRAMMAR:
    topic, created = GrammarTopic.objects.update_or_create(
        slug=data['slug'],
        defaults={
            'name': data['name'],
            'name_es': data['name_es'],
            'level': 'A1',
            'order': data['order'],
            'description': data['description'],
            'pattern': data['pattern'],
            'examples': data['examples'],
            'rules': data['rules'],
            'exceptions': [],
            'estimated_time': 30,
        }
    )
    
    # Create lessons
    for i, (lesson_name, explanation, examples) in enumerate(data['lessons'], 1):
        GrammarLesson.objects.update_or_create(
            topic=topic,
            order=i,
            defaults={
                'name': lesson_name,
                'explanation': explanation,
                'examples': examples,
                'exercises': [],
                'estimated_time': 10,
            }
        )
    
    status = "✅ Created" if created else "🔄 Updated"
    print(f"  {status}: {topic}")

print(f"\n📚 Total A1 topics: {GrammarTopic.objects.filter(level='A1').count()}")
print(f"📖 Total A1 lessons: {GrammarLesson.objects.filter(topic__level='A1').count()}")
print("\n✅ A1 Grammar seeded!")
