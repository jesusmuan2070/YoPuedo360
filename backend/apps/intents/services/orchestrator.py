"""
Learning Orchestrator - Motor pedagógico central
Coordina Intent + Grammar para generar contenido de aprendizaje
"""

from apps.intents.models import CommunicativeIntent, IntentRealization
from apps.grammar.models import GrammarUnit, GrammarInMilestone
from apps.scenarios.models import Milestone
from apps.ai_services.clients.openai_client import OpenAIClient

# Language code to name mapping
LANGUAGE_NAMES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'pt': 'Portuguese',
    'it': 'Italian',
}


class LearningOrchestrator:
    """
    Orquestador central que decide QUÉ mostrar al usuario.
    
    Flujo:
    1. Usuario entra a Milestone
    2. Sistema determina Intents relevantes
    3. Para cada Intent, obtiene/genera ejemplos
    4. Identifica Grammar necesaria
    5. Obtiene/genera ejemplos de Grammar
    6. Ensambla contenido final
    """
    
    def __init__(self):
        self.ai_client = OpenAIClient()
    
    def get_learning_content(self, user, milestone):
        """
        Entrada principal: Usuario + Milestone
        Salida: Contenido completo para aprender
        
        Args:
            user: Usuario actual
            milestone: Milestone seleccionado
            
        Returns:
            {
                'intents': [IntentRealization],
                'grammar': [GrammarInMilestone],
                'exercises': [...],
                'progress': {...}
            }
        """
        
        # PASO 1: Obtener intents relevantes
        available_intents = self._get_available_intents(milestone)
        
        # Validar que hay intents disponibles
        if not available_intents:
            return {
                'error': True,
                'message': f'No hay intents disponibles para este milestone. Scenario: {milestone.scenario.slug}',
                'current_intent': None,
                'target_phrases': [],
                'supporting_grammar': [],
                'exercises': [],
                'progress': {'total': 0, 'completed': 0, 'percentage': 0}
            }
        
        # PASO 2: Determinar siguiente intent según progreso
        next_intent = self._get_next_intent(user, milestone, available_intents)
        
        # Validar que se encontró un intent
        if not next_intent:
            return {
                'error': True,
                'message': 'No se pudo determinar el siguiente intent',
                'current_intent': None,
                'target_phrases': [],
                'supporting_grammar': [],
                'exercises': [],
                'progress': self._get_progress(user, milestone)
            }
        
        # PASO 3: Obtener/generar realización del intent
        intent_realization = self._get_or_generate_intent_realization(
            next_intent, 
            milestone,
            user  # Pass user for language
        )
        
        # PASO 4: Identificar grammar necesaria
        required_grammar = self._get_required_grammar(next_intent, milestone)
        
        # PASO 5: Obtener/generar ejemplos de grammar contextuales
        grammar_examples = self._get_or_generate_grammar_examples(required_grammar, milestone)
        
        # PASO 6: Ensamblar contenido
        return {
            'current_intent': intent_realization,
            'target_phrases': intent_realization.example_chunks,
            'supporting_grammar': grammar_examples,
            'exercises': self._generate_exercises(intent_realization),
            'progress': self._get_progress(user, milestone)
        }
    
    def _get_available_intents(self, milestone):
        """
        Devuelve todos los intents disponibles para este milestone.
        Usa coverage map para filtrar relevantes.
        """
        from .intent_coverage import is_intent_relevant
        
        # Todos los intents del nivel
        level_intents = CommunicativeIntent.objects.filter(
            level=milestone.level,
            is_core=True
        ).order_by('cefr_rank')
        
        # Filtrar por relevancia
        relevant = [
            intent for intent in level_intents
            if is_intent_relevant(intent, milestone)
        ]
        
        return relevant
    
    def _get_next_intent(self, user, milestone, available_intents):
        """
        Determina cuál intent mostrar según progreso del usuario.
        """
        from apps.intents.models import UserIntentProgress
        
        # Buscar primer intent no masterizado
        for intent in available_intents:
            progress = UserIntentProgress.objects.filter(
                user=user,
                intent=intent
            ).first()
            
            # No existe o no está masterizado
            if not progress or progress.status != 'mastered':
                return intent
        
        # Todos masterizados → devolver primero para repaso
        return available_intents[0] if available_intents else None
    
    def _get_or_generate_intent_realization(self, intent, milestone, user):
        """
        Obtiene o genera IntentRealization on-the-fly.
        
        Args:
            intent: CommunicativeIntent to realize
            milestone: Milestone context
            user: User (for target_language)
        """
        # Primero intentamos obtener el existente
        realization = IntentRealization.objects.filter(
            intent=intent,
            milestone=milestone
        ).first()
        
        if realization:
            return realization
        
        # No existe → Generar con AI
        print(f"🤖 Generating intent realization: {intent.name} in {milestone.name}")
        examples = self._generate_intent_examples_ai(intent, milestone, user)
        
        # Usar get_or_create para evitar race condition
        # Si otra petición creó el registro mientras generábamos con AI,
        # simplemente obtenemos ese registro en lugar de fallar
        realization, created = IntentRealization.objects.get_or_create(
            intent=intent,
            milestone=milestone,
            defaults={
                'example_chunks': examples['chunks'],
                'difficulty': examples.get('difficulty', 2),
                'estimated_time': examples.get('time', 10),
                'priority': self._calculate_priority(intent, milestone)
            }
        )
        
        # Si ya existía (otra petición lo creó), podemos actualizar con nuestros datos
        # (opcional, por ahora usamos lo que ya existe)
        if not created:
            print(f"ℹ️ Intent realization already existed (created by parallel request)")
        
        return realization
    
    def _get_required_grammar(self, intent, milestone):
        """
        Identifica qué grammar necesita este intent.
        """
        if not intent:
            return []
            
        from apps.intents.models import IntentGrammarDependency
        
        # Grammar asociada al intent
        dependencies = IntentGrammarDependency.objects.filter(
            intent=intent,
            is_critical=True
        ).select_related('grammar').order_by('order')
        
        return [dep.grammar for dep in dependencies]
    
    def _get_or_generate_grammar_examples(self, grammar_units, milestone):
        """
        Obtiene o genera ejemplos de grammar en el milestone.
        """
        results = []
        
        for grammar in grammar_units:
            # Buscar existente
            example = GrammarInMilestone.objects.filter(
                grammar=grammar,
                milestone=milestone
            ).first()
            
            if not example:
                # Generar on-the-fly
                print(f"🤖 Generating grammar example: {grammar.name} in {milestone.name}")
                
                ai_examples = self._generate_grammar_examples_ai(grammar, milestone)
                
                example = GrammarInMilestone.objects.create(
                    grammar=grammar,
                    milestone=milestone,
                    context_example=ai_examples['examples'],
                    importance_weight=ai_examples.get('importance', 3)
                )
            
            results.append(example)
        
        return results
    
    def _generate_intent_examples_ai(self, intent, milestone, user):
        """
        Genera ejemplos de intent con AI.
        
        Args:
            intent: CommunicativeIntent
            milestone: Milestone context
            user: User (for target_language)
        """
        # Get target language from user's learning profile (REQUIRED)
        if not user:
            raise ValueError("User is required for content generation")
        
        if not hasattr(user, 'learning_profile'):
            raise ValueError(f"User {user.username} does not have a learning profile configured")
        
        target_lang_code = user.learning_profile.target_language
        if not target_lang_code:
            raise ValueError(f"User {user.username} does not have target_language configured")
        
        target_lang = LANGUAGE_NAMES.get(target_lang_code, 'English')
        
        prompt = f"""Generate 3-4 example phrases IN {target_lang.upper()} for teaching {target_lang} to learners.

Communicative intent: "{intent.name}"
Context: "{milestone.scenario.name} - {milestone.name}" at level {milestone.level}.

IMPORTANT: All examples must be in {target_lang.upper()}, not in any other language.

Return JSON:
{{
  "chunks": ["Example 1 in {target_lang}", "Example 2 in {target_lang}", "Example 3 in {target_lang}"],
  "difficulty": 1-5,
  "time": 5-15
}}"""

        response = self.ai_client.complete_json(
            prompt=prompt,
            temperature=0.3,
            max_tokens=200
        )
        
        return response
    
    def _generate_grammar_examples_ai(self, grammar, milestone):
        """
        Genera ejemplos de grammar con AI.
        """
        prompt = f"""Generate 3-4 example sentences using "{grammar.name}" ({grammar.form})
in the context of "{milestone.scenario.name} - {milestone.name}".

Return JSON:
{{
  "examples": ["Example 1", "Example 2"],
  "importance": 1-5
}}"""

        response = self.ai_client.complete_json(
            prompt=prompt,
            temperature=0.3,
            max_tokens=200
        )
        
        return response
    
    def _calculate_priority(self, intent, milestone):
        """
        Calcula prioridad del intent en este milestone.
        """
        # Survival intents siempre alta prioridad
        if intent.category == 'survival':
            return 1
        
        # Usar cefr_rank como base
        return min(intent.cefr_rank, 3)
    
    def _generate_exercises(self, intent_realization):
        """
        Genera ejercicios para practicar.
        TODO: Implementar generación de ejercicios
        """
        return []
    
    def _get_progress(self, user, milestone):
        """
        Calcula progreso del usuario en este milestone.
        """
        from apps.intents.models import UserIntentProgress
        
        # Intents disponibles
        available = self._get_available_intents(milestone)
        
        # Intents masterizados
        mastered = UserIntentProgress.objects.filter(
            user=user,
            intent__in=available,
            status='mastered'
        ).count()
        
        return {
            'total': len(available),
            'completed': mastered,
            'percentage': round((mastered / len(available) * 100) if available else 0)
        }


# Instancia global
orchestrator = LearningOrchestrator()
