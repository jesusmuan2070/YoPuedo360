"""
Progress API Views
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.memory_palace.models import Scenario, Milestone
from .models import UserMilestoneProgress, UserExerciseAttempt
from .serializers import (
    UserMilestoneProgressSerializer,
    ScenarioProgressSerializer,
    MilestoneSimpleSerializer,
    StartMilestoneSerializer,
    CompleteMilestoneSerializer,
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_progress(request):
    """
    GET /api/v1/progress/
    Get overall progress for the authenticated user
    """
    user = request.user
    
    # Get all milestone progress
    milestone_progress = UserMilestoneProgress.objects.filter(
        user=user
    ).select_related('milestone', 'milestone__scenario')
    
    # Summary stats
    total_completed = milestone_progress.filter(status='completed').count()
    total_in_progress = milestone_progress.filter(status='in_progress').count()
    total_xp = sum(mp.xp_earned for mp in milestone_progress)
    
    # Recent activity
    recent = milestone_progress.order_by('-last_activity')[:5]
    
    return Response({
        'summary': {
            'milestones_completed': total_completed,
            'milestones_in_progress': total_in_progress,
            'total_xp': total_xp,
        },
        'recent_activity': UserMilestoneProgressSerializer(recent, many=True).data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def scenario_progress(request, scenario_slug):
    """
    GET /api/v1/progress/scenario/<slug>/
    Get progress for a specific scenario
    """
    user = request.user
    
    try:
        scenario = Scenario.objects.get(slug=scenario_slug)
    except Scenario.DoesNotExist:
        return Response({'error': 'Scenario not found'}, status=404)
    
    # Get progress summary
    progress = UserMilestoneProgress.get_scenario_progress(user, scenario)
    
    # Get milestone details
    milestones = Milestone.objects.filter(scenario=scenario).order_by('level', 'order')
    
    milestone_data = []
    for m in milestones:
        mp = UserMilestoneProgress.objects.filter(user=user, milestone=m).first()
        milestone_data.append({
            'id': m.id,
            'name': m.name,
            'level': m.level,
            'order': m.order,
            'estimated_time': m.estimated_time,
            'status': mp.status if mp else 'not_started',
            'progress_percent': mp.progress_percent if mp else 0,
            'best_score': mp.best_score if mp else 0,
        })
    
    return Response({
        'scenario': {
            'id': scenario.id,
            'name': scenario.name,
            'slug': scenario.slug,
            'icon': scenario.icon,
        },
        'progress': progress,
        'milestones': milestone_data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_milestones(request, scenario_slug):
    """
    GET /api/v1/progress/scenario/<slug>/pending/
    Get only pending (not completed) milestones for a scenario
    """
    user = request.user
    
    try:
        scenario = Scenario.objects.get(slug=scenario_slug)
    except Scenario.DoesNotExist:
        return Response({'error': 'Scenario not found'}, status=404)
    
    pending = UserMilestoneProgress.get_pending_milestones(user, scenario)
    
    return Response({
        'scenario_slug': scenario_slug,
        'pending_count': pending.count(),
        'milestones': MilestoneSimpleSerializer(pending, many=True).data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def next_milestone(request, scenario_slug):
    """
    GET /api/v1/progress/scenario/<slug>/next/
    Get the next milestone to work on
    """
    user = request.user
    
    try:
        scenario = Scenario.objects.get(slug=scenario_slug)
    except Scenario.DoesNotExist:
        return Response({'error': 'Scenario not found'}, status=404)
    
    next_m = UserMilestoneProgress.get_next_milestone(user, scenario)
    
    if not next_m:
        return Response({
            'message': 'All milestones completed!',
            'milestone': None,
        })
    
    return Response({
        'milestone': MilestoneSimpleSerializer(next_m).data,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_milestone(request):
    """
    POST /api/v1/progress/start/
    Start working on a milestone
    Body: { "milestone_id": 123 }
    """
    user = request.user
    serializer = StartMilestoneSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    milestone_id = serializer.validated_data['milestone_id']
    
    try:
        milestone = Milestone.objects.get(id=milestone_id)
    except Milestone.DoesNotExist:
        return Response({'error': 'Milestone not found'}, status=404)
    
    # Get or create progress record
    progress, created = UserMilestoneProgress.objects.get_or_create(
        user=user,
        milestone=milestone,
    )
    
    # Mark as started
    progress.start()
    
    return Response({
        'message': 'Milestone started',
        'progress': UserMilestoneProgressSerializer(progress).data,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_milestone(request):
    """
    POST /api/v1/progress/complete/
    Complete a milestone
    Body: { "milestone_id": 123, "score": 85, "time_spent_seconds": 300 }
    """
    user = request.user
    serializer = CompleteMilestoneSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    data = serializer.validated_data
    milestone_id = data['milestone_id']
    
    try:
        milestone = Milestone.objects.get(id=milestone_id)
    except Milestone.DoesNotExist:
        return Response({'error': 'Milestone not found'}, status=404)
    
    # Get progress record
    progress, created = UserMilestoneProgress.objects.get_or_create(
        user=user,
        milestone=milestone,
    )
    
    # Mark as completed
    progress.complete(
        score=data.get('score', 100),
        time_spent=data.get('time_spent_seconds', 0)
    )
    
    return Response({
        'message': 'Milestone completed!',
        'xp_earned': progress.xp_earned,
        'progress': UserMilestoneProgressSerializer(progress).data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def milestone_detail(request, milestone_id):
    """
    GET /api/v1/progress/milestone/<id>/
    Get progress for a specific milestone
    """
    user = request.user
    
    try:
        milestone = Milestone.objects.get(id=milestone_id)
    except Milestone.DoesNotExist:
        return Response({'error': 'Milestone not found'}, status=404)
    
    progress = UserMilestoneProgress.objects.filter(
        user=user, 
        milestone=milestone
    ).first()
    
    if not progress:
        return Response({
            'milestone_id': milestone_id,
            'status': 'not_started',
            'progress': None,
        })
    
    return Response({
        'milestone_id': milestone_id,
        'status': progress.status,
        'progress': UserMilestoneProgressSerializer(progress).data,
    })
