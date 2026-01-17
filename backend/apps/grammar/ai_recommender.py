"""
AI Grammar Recommender Service
Usa AI para determinar QUÉ gramática es relevante para cada milestone dinámicamente.

NO hardcodea la conexión - la determina según:
- Nivel CEFR del milestone
- Vocabulario usado en el milestone
- Contexto/dominio del scenario
- Estructura de las oraciones necesarias
"""

from typing import List, Dict, Any
from apps.grammar.models import GrammarUnit, GrammarInMiles

tone
from apps.scenarios.models import Milestone
from apps.ai_services.clients.openai_client import OpenAIClient


class AIGrammarRecommender:
    """
    Determina automáticamente qué gramática es relevante para un milestone
    usando análisis AI.
    """
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self._client = None
    
    @property
    def client(self) -> OpenAIClient:
        if self._client is None:
            self._client = OpenAIClient(model=self.model)
        return self._client
    
    def recommend_grammar_for_milestone(
        self,
        milestone: Milestone,
        target_language: str = 'en'
    ) -> List[Dict[str, Any]]:
        """
        Determina qué estructuras gramaticalesecesita un usuario
        para completar este milestone.
        
        Returns:
            List[Dict] con:
            - grammar_slug: str
            - importance_weight: int (1-5)
            - is_primary_focus: bool
            - context_example: str
            - suggested_order: int
        """
        
        # Obtener todas las grammar units disponibles para este nivel
        available_grammar = self._get_available_grammar(
            milestone.difficulty_level,  # Asumiendo campo level en milestone
            target_language
        )
        
        # Preparar contexto del milestone
        milestone_context = {
            'name': milestone.name,
            'description': milestone.description,
            'level': milestone.difficulty_level,
            'scenario': milestone.scenario.name,
            'domain': [t.value for t in milestone.scenario.tags.filter(type='domain')],
            'estimated_vocab_count': milestone.estimated_vocab_count,
        }
        
        # Usar AI para determinar qué gramática es relevante
        recommendations = self._analyze_grammar_needs(
            milestone_context,
            available_grammar
        )
        
        return recommendations
    
    def _get_available_grammar(
        self,
        level: str,
        target_language: str
    ) -> List[Dict]:
        """
        Obtiene gramática disponible para este nivel y idioma.
        """
        # Get grammar AT or BELOW this level
        level_hierarchy = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        current_index = level_hierarchy.index(level)
        valid_levels = level_hierarchy[:current_index + 1]
        
        grammar_units = GrammarUnit.objects.filter(
            target_language=target_language,
            level__in=valid_levels
        ).values(
            'id', 'slug', 'name', 'gramatical_category',
            'form', 'meaning_en', 'level'
        )
        
        return list(grammar_units)
    
    def _analyze_grammar_needs(
        self,
        milestone_context: Dict,
        available_grammar: List[Dict]
    ) -> List[Dict]:
        """
        Usa AI para determinar qué gramática es crítica para este milestone.
        """
        
        system_prompt = """Eres un experto en pedagogía de idiomas y diseño curricular.
Tu tarea es analizar un milestone de aprendizaje y determinar QUÉ estructuras gramaticales
son necesarias para que un estudiante complete ese milestone exitosamente.

Considera:
1. El nivel CEFR del milestone
2. El contexto/dominio (restaurant, airport, etc.)
3. Qué tipo de oraciones necesitará formar el estudiante
4. Cuáles son CRÍTICAS vs opcionales

Devuelve SOLO las estructuras más relevantes (máximo 5), ordenadas por importancia."""
        
        user_prompt = f"""Analiza este milestone:

Nombre: {milestone_context['name']}
Descripción: {milestone_context['description']}
Nivel: {milestone_context['level']}
Escenario: {milestone_context['scenario']}
Dominio: {', '.join(milestone_context['domain'])}

Gramática disponible para este nivel:
{self._format_grammar_list(available_grammar)}

Determina las estructuras gramaticales MÁS IMPORTANTES para este milestone.
Para cada una, explica POR QUÉ es importante y da un ejemplo EN CONTEXTO.

Devuelve JSON:
{{
  "recommendations": [
    {{
      "grammar_slug": "can-infinitive",
      "importance_weight": 5,
      "is_primary_focus": true,
      "reasoning": "El estudiante necesita hacer peticiones en el restaurante",
      "context_example": "Can I have a coffee? Can I see the menu?",
      "suggested_order": 1
    }},
    ...
  ]
}}
"""
        
        try:
            response = self.client.complete_json(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.2,
                max_tokens=1500
            )
            
            return response.get('recommendations', [])
            
        except Exception as e:
            print(f"AI Grammar Recommender error: {e}")
            return []
    
    def _format_grammar_list(self, grammar_units: List[Dict]) -> str:
        """Formatea la lista de gramática para el prompt."""
        lines = []
        for g in grammar_units:
            lines.append(
                f"- [{g['slug']}] {g['name']} ({g['level']}) - {g['form']}"
            )
        return '\n'.join(lines)
    
    def auto_populate_milestone_grammar(
        self,
        milestone: Milestone,
        target_language: str = 'en',
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Automáticamente pobla las conexiones GrammarInMilestone
        para un milestone usando AI.
        
        Args:
            milestone: Milestone instance
            target_language: Idioma objetivo
            dry_run: Si True, no crea los registros, solo retorna recomendaciones
        
        Returns:
            Dict con estadísticas y recomendaciones
        """
        recommendations = self.recommend_grammar_for_milestone(
            milestone,
            target_language
        )
        
        created_count = 0
        results = []
        
        for rec in recommendations:
            try:
                grammar = GrammarUnit.objects.get(
                    slug=rec['grammar_slug'],
                    target_language=target_language
                )
                
                if not dry_run:
                    connection, created = GrammarInMilestone.objects.update_or_create(
                        grammar=grammar,
                        milestone=milestone,
                        defaults={
                            'importance_weight': rec['importance_weight'],
                            'is_primary_focus': rec['is_primary_focus'],
                            'context_example': rec['context_example'],
                            'introduction_order': rec['suggested_order'],
                        }
                    )
                    
                    if created:
                        created_count += 1
                
                results.append({
                    'grammar': grammar.name,
                    'slug': rec['grammar_slug'],
                    'importance': rec['importance_weight'],
                    'primary': rec['is_primary_focus'],
                    'reasoning': rec.get('reasoning', ''),
                    'example': rec['context_example'],
                    'created': not dry_run
                })
                
            except GrammarUnit.DoesNotExist:
                print(f"  ⚠️  Grammar '{rec['grammar_slug']}' not found")
        
        return {
            'milestone': milestone.name,
            'total_recommendations': len(recommendations),
            'created': created_count if not dry_run else 0,
            'dry_run': dry_run,
            'results': results
        }


# ==================================
# CLI PARA POBLAR MILESTONES
# ==================================

def populate_all_milestones_with_ai():
    """
    Comando para poblar TODOS los milestones con gramática usando AI.
    """
    import os
    import sys
    import django
    
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yopuedo360.settings')
    django.setup()
    
    from apps.scenarios.models import Milestone
    
    recommender = AIGrammarRecommender()
    
    # Filtrar solo milestones A1-A2 para empezar
    milestones = Milestone.objects.filter(
        difficulty_level__in=['A1', 'A2']
    ).select_related('scenario')[:10]  # Primeros 10 para prueba
    
    print(f"🤖 Poblando {milestones.count()} milestones con AI...\n")
    
    for milestone in milestones:
        print(f"\n📍 {milestone.scenario.name} - {milestone.name}")
        
        result = recommender.auto_populate_milestone_grammar(
            milestone,
            target_language='en',
            dry_run=False  # Cambiar a True para solo ver recomendaciones
        )
        
        print(f"   Recomendaciones: {result['total_recommendations']}")
        print(f"   Creadas: {result['created']}")
        
        for r in result['results']:
            icon = '⭐' if r['primary'] else '  '
            print(f"   {icon} {r['grammar']} (weight: {r['importance']})")
            print(f"      Ejemplo: {r['example']}")
            if r.get('reasoning'):
                print(f"      Razón: {r['reasoning']}")
    
    print("\n✅ Población completada")


if __name__ == '__main__':
    populate_all_milestones_with_ai()
