"""
API Views for Intent-First Learning System
Provides endpoints for scenario browsing, milestone content, and intent realizations
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.scenarios.models import Scenario, Milestone
from apps.intents.models import CommunicativeIntent, IntentRealization, UserIntentProgress
from apps.intents.services.orchestrator import orchestrator


@api_view(['GET'])
def get_scenarios(request):
    """
    Get all scenarios with progress info for user
    Used by: ScenarioList, WorldMap
    """
    scenarios = Scenario.objects.all().select_related().prefetch_related('milestones')
    
    data = []
    for scenario in scenarios:
        milestones_count = scenario.milestones.count()
        
        # TODO: Calculate user progress
        data.append({
            'id': scenario.id,
            'slug': scenario.slug,
            'name': scenario.name,
            'icon': scenario.icon,
            'description': scenario.description,
            'difficulty_min': scenario.difficulty_min,
            'difficulty_max': scenario.difficulty_max,
            'milestones_count': milestones_count,
            'tags': list(scenario.tags.values_list('slug', flat=True))
        })
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_scenario_progress(request, slug):
    """
    Get scenario details with milestones and user progress
    Used by: ScenarioPage
    
    Format expected by frontend:
    {
        scenario: {...},
        milestones: [{id, name, status, level, estimated_time, best_score}],
        progress: {completed, total, percent}
    }
    """
    scenario = get_object_or_404(Scenario, slug=slug)
    milestones = scenario.milestones.filter(level='A1').order_by('order')
    
    milestone_data = []
    completed_count = 0
    
    for milestone in milestones:
        # TODO: Get actual user progress
        # For now, all milestones are 'not_started'
        milestone_data.append({
            'id': milestone.id,
            'name': milestone.name,
            'level': milestone.level,
            'estimated_time': milestone.estimated_time,
            'status': 'not_started',  # TODO: Get from UserMilestoneProgress
            'best_score': 0,  # TODO: Get from UserMilestoneProgress
        })
    
    return Response({
        'scenario': {
            'id': scenario.id,
            'slug': scenario.slug,
            'name': scenario.name,
            'icon': scenario.icon,
            'description': scenario.description,
        },
        'milestones': milestone_data,
        'progress': {
            'completed': completed_count,
            'total': len(milestone_data),
            'percent': round((completed_count / len(milestone_data) * 100) if milestone_data else 0)
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_milestone(request, milestone_id):
    """
    Mark milestone as started for user
    Used by: ScenarioPage when user clicks milestone
    """
    milestone = get_object_or_404(Milestone, id=milestone_id)
    
    # TODO: Create/update UserMilestoneProgress
    # For now, just return success
    
    return Response({
        'success': True,
        'milestone_id': milestone_id,
        'status': 'in_progress'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_milestone_content(request, milestone_id):
    """
    Get learning content for a milestone (Intent + Grammar + Exercises)
    Uses the orchestrator to generate/retrieve content
    
    Returns:
    {
        current_intent: {...},
        target_phrases: ["phrase 1", "phrase 2"],
        supporting_grammar: [{name, examples}],
        exercises: [],
        progress: {total, completed, percentage}
    }
    """
    milestone = get_object_or_404(Milestone, id=milestone_id)
    user = request.user
    
    # Use orchestrator to get learning content
    content = orchestrator.get_learning_content(user, milestone)
    
    # Format for frontend
    response_data = {
        'milestone': {
            'id': milestone.id,
            'name': milestone.name,
            'level': milestone.level,
        },
        'current_intent': {
            'id': content['current_intent'].intent.id if content.get('current_intent') else None,
            'name': content['current_intent'].intent.name if content.get('current_intent') else None,
            'category': content['current_intent'].intent.category if content.get('current_intent') else None,
        },
        'target_phrases': content.get('target_phrases', []),
        'supporting_grammar': [
            {
                'name': item.grammar.name if hasattr(item, 'grammar') else item.name,
                'form': item.grammar.form if hasattr(item, 'grammar') else item.form,
                'examples': (item.context_example if hasattr(item, 'context_example') and item.context_example else (item.grammar.examples if hasattr(item, 'grammar') else item.examples))[:3],
            }
            for item in content.get('supporting_grammar', [])
        ],
        'exercises': content.get('exercises', []),
        'progress': content.get('progress', {})
    }
    
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_intent(request, intent_id):
    """
    Mark an intent as practiced/completed
    Updates UserIntentProgress
    
    Body: {
        milestone_id: int,
        score: int (0-100)
    }
    """
    user = request.user
    intent = get_object_or_404(CommunicativeIntent, id=intent_id)
    milestone_id = request.data.get('milestone_id')
    score = request.data.get('score', 0)
    
    # Update or create progress
    progress, created = UserIntentProgress.objects.get_or_create(
        user=user,
        intent=intent,
        defaults={'status': 'practicing'}
    )
    
    # Update progress
    progress.times_practiced += 1
    progress.last_score = score
    
    # Update status based on score
    if score >= 80:
        progress.status = 'mastered'
    elif score >= 50:
        progress.status = 'practicing'
    else:
        progress.status = 'ready'
    
    progress.save()
    
    return Response({
        'success': True,
        'status': progress.status,
        'times_practiced': progress.times_practiced,
        'last_score': progress.last_score,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_progress(request):
    """
    Get overall user progress (all intents)
    Used by: Dashboard, Profile
    """
    user = request.user
    
    progress = UserIntentProgress.objects.filter(user=user).select_related('intent')
    
    stats = {
        'total_intents': CommunicativeIntent.objects.filter(level='A1').count(),
        'mastered': progress.filter(status='mastered').count(),
        'practicing': progress.filter(status='practicing').count(),
        'ready': progress.filter(status='ready').count(),
    }
    
    return Response(stats)
