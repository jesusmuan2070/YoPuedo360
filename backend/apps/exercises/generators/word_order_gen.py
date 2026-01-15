"""
Word Order Exercise Generator
Generates word ordering exercises from sentences
"""
from .base import ExerciseGeneratorBase
from ..models.word_order import WordOrderExercise


class WordOrderGenerator(ExerciseGeneratorBase):
    """
    Generates Word Order exercises from sentences or grammar topics.
    """
    
    # Sentences por nivel y gramática
    SENTENCE_TEMPLATES = {
        'A1': {
            'a1-verb-to-be': [
                ("I am a student", "Soy estudiante"),
                ("She is a teacher", "Ella es maestra"),
                ("They are my friends", "Ellos son mis amigos"),
                ("He is from Mexico", "Él es de México"),
                ("We are happy", "Estamos felices"),
                ("It is a beautiful day", "Es un día hermoso"),
                ("You are very kind", "Eres muy amable"),
                ("I am not tired", "No estoy cansado"),
                ("Is she your sister?", "¿Es ella tu hermana?"),
                ("Are you ready?", "¿Estás listo?"),
            ],
            'a1-present-simple': [
                ("I work every day", "Trabajo todos los días"),
                ("She speaks English", "Ella habla inglés"),
                ("They live in Madrid", "Ellos viven en Madrid"),
                ("He plays football", "Él juega fútbol"),
                ("I eat breakfast at eight", "Desayuno a las ocho"),
                ("She doesn't like coffee", "A ella no le gusta el café"),
                ("Do you speak Spanish?", "¿Hablas español?"),
                ("He works in an office", "Él trabaja en una oficina"),
            ],
            'a1-can-cant': [
                ("I can swim", "Puedo nadar"),
                ("She can speak French", "Ella puede hablar francés"),
                ("He can't drive", "Él no puede manejar"),
                ("Can you help me?", "¿Puedes ayudarme?"),
                ("I can play guitar", "Puedo tocar guitarra"),
                ("We can't understand", "No podemos entender"),
                ("Can I have the menu?", "¿Puedo tener el menú?"),
            ],
            'a1-there-is-are': [
                ("There is a book on the table", "Hay un libro en la mesa"),
                ("There are two cats", "Hay dos gatos"),
                ("Is there a bathroom?", "¿Hay un baño?"),
                ("There isn't any milk", "No hay leche"),
                ("There are many people here", "Hay muchas personas aquí"),
            ],
            'a1-basic-questions': [
                ("What is your name?", "¿Cuál es tu nombre?"),
                ("Where do you live?", "¿Dónde vives?"),
                ("How are you?", "¿Cómo estás?"),
                ("When is the party?", "¿Cuándo es la fiesta?"),
                ("Who is that man?", "¿Quién es ese hombre?"),
                ("Why are you sad?", "¿Por qué estás triste?"),
            ],
            'a1-articles': [
                ("I have a car", "Tengo un carro"),
                ("She is an engineer", "Ella es ingeniera"),
                ("The book is interesting", "El libro es interesante"),
                ("I want a coffee please", "Quiero un café por favor"),
            ],
            'a1-possessives': [
                ("This is my phone", "Este es mi teléfono"),
                ("Her name is Maria", "Su nombre es María"),
                ("Their house is big", "Su casa es grande"),
                ("Your idea is great", "Tu idea es genial"),
            ],
            'a1-prepositions-place': [
                ("The book is on the table", "El libro está en la mesa"),
                ("She lives in Madrid", "Ella vive en Madrid"),
                ("I am at the office", "Estoy en la oficina"),
                ("The cat is under the bed", "El gato está debajo de la cama"),
            ],
        }
    }
    
    def generate(self, level='A1', grammar_topic=None, milestone=None, **kwargs):
        """
        Generate a single Word Order exercise.
        """
        sentences = self._get_sentences(level, grammar_topic)
        
        if not sentences:
            return None
        
        import random
        sentence, translation = random.choice(sentences)
        
        exercise = WordOrderExercise.objects.create(
            sentence=sentence,
            translation=translation,
            level=level,
            grammar_topic=grammar_topic,
            milestone=milestone,
            **kwargs
        )
        
        return exercise
    
    def generate_bulk(self, count=10, level='A1', grammar_topic=None, **kwargs):
        """
        Generate multiple Word Order exercises.
        """
        sentences = self._get_sentences(level, grammar_topic)
        exercises = []
        
        import random
        selected = random.sample(sentences, min(count, len(sentences)))
        
        for sentence, translation in selected:
            exercise = WordOrderExercise.objects.create(
                sentence=sentence,
                translation=translation,
                level=level,
                grammar_topic=grammar_topic,
                **kwargs
            )
            exercises.append(exercise)
        
        return exercises
    
    def generate_for_grammar_topic(self, grammar_topic):
        """
        Generate all exercises for a grammar topic.
        """
        level = grammar_topic.level
        topic_slug = grammar_topic.slug
        
        sentences = self._get_sentences(level, topic_slug)
        exercises = []
        
        for sentence, translation in sentences:
            exercise, created = WordOrderExercise.objects.get_or_create(
                sentence=sentence,
                level=level,
                defaults={
                    'translation': translation,
                    'grammar_topic': grammar_topic,
                }
            )
            if created:
                exercises.append(exercise)
        
        return exercises
    
    def _get_sentences(self, level, grammar_topic=None):
        """Get sentences for a level/topic"""
        level_sentences = self.SENTENCE_TEMPLATES.get(level, {})
        
        if grammar_topic:
            # Si es un objeto, obtener el slug
            topic_slug = grammar_topic.slug if hasattr(grammar_topic, 'slug') else grammar_topic
            return level_sentences.get(topic_slug, [])
        
        # Si no hay topic, devolver todas las del nivel
        all_sentences = []
        for topic_sentences in level_sentences.values():
            all_sentences.extend(topic_sentences)
        return all_sentences
