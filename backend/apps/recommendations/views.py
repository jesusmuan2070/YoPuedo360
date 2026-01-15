"""
Recommendation API Views
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import RecommendationEngine
from .serializers import RecommendationResultSerializer


class RecommendedScenariosView(APIView):
    """
    Get personalized scenario recommendations.
    GET /api/v1/recommendations/scenarios/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        include_completed = request.query_params.get('include_completed', 'false').lower() == 'true'
        
        engine = RecommendationEngine()
        result = engine.recommend(
            user=request.user,
            limit=limit,
            include_completed=include_completed
        )
        
        serializer = RecommendationResultSerializer(result)
        return Response(serializer.data)


class SimilarScenariosView(APIView):
    """
    Get scenarios similar to a given one.
    GET /api/v1/recommendations/similar/<scenario_id>/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, scenario_id):
        from apps.memory_palace.models import Scenario
        
        try:
            scenario = Scenario.objects.get(id=scenario_id)
        except Scenario.DoesNotExist:
            return Response(
                {'error': 'Scenario not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        limit = int(request.query_params.get('limit', 5))
        
        engine = RecommendationEngine()
        similar = engine.get_similar_scenarios(scenario, limit=limit)
        
        from .serializers import RecommendedScenarioSerializer
        serializer = RecommendedScenarioSerializer(similar, many=True)
        
        return Response({
            'base_scenario': scenario.name,
            'similar_scenarios': serializer.data
        })
