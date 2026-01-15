"""
Onboarding API views.
Handles registration, onboarding flow, and VAK assessment.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .models import OnboardingStep, VAKAssessmentQuestion
from .serializers import (
    UserRegistrationSerializer,
    OnboardingStepSerializer,
    VAKAssessmentQuestionSerializer,
    OnboardingStepCompleteSerializer,
    UserOnboardingProgressSerializer,
    VAKResultSerializer,
)
from .services import OnboardingService


User = get_user_model()


class RegisterView(APIView):
    """
    User registration endpoint.
    POST /api/v1/auth/register/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                'onboarding': {
                    'current_step': 1,
                    'is_completed': False,
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OnboardingStepsView(APIView):
    """
    Get all onboarding steps.
    GET /api/v1/onboarding/steps/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        steps = OnboardingStep.objects.filter(is_active=True).order_by('order')
        serializer = OnboardingStepSerializer(steps, many=True)
        
        # Get user's progress
        progress = OnboardingService.get_user_progress(request.user)
        
        return Response({
            'steps': serializer.data,
            'current_step': progress.current_step if progress else 1,
            'completed_steps': progress.completed_steps if progress else [],
            'is_completed': progress.is_completed if progress else False,
        })


class OnboardingProgressView(APIView):
    """
    Get user's onboarding progress.
    GET /api/v1/onboarding/progress/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        progress = OnboardingService.get_user_progress(request.user)
        
        if not progress:
            return Response({
                'current_step': 1,
                'completed_steps': [],
                'collected_data': {},
                'is_completed': False,
            })
        
        serializer = UserOnboardingProgressSerializer(progress)
        return Response(serializer.data)


class CompleteStepView(APIView):
    """
    Complete an onboarding step and save data.
    POST /api/v1/onboarding/complete-step/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = OnboardingStepCompleteSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        step_type = serializer.validated_data['step_type']
        data = serializer.validated_data['data']
        
        # Save step data
        progress = OnboardingService.save_step_data(
            request.user,
            step_type,
            data
        )
        
        return Response({
            'success': True,
            'current_step': progress.current_step,
            'completed_steps': progress.completed_steps,
        })


class VAKAssessmentView(APIView):
    """
    Get VAK assessment questions.
    GET /api/v1/onboarding/vak-assessment/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        questions = OnboardingService.get_default_vak_questions()
        return Response({
            'questions': questions,
            'total_questions': len(questions),
            'instructions': 'Choose the option that best describes how you learn.',
        })


class SubmitVAKAssessmentView(APIView):
    """
    Submit VAK assessment answers and get results.
    POST /api/v1/onboarding/submit-vak/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        answers = request.data.get('answers', [])
        
        if not answers:
            return Response(
                {'error': 'No answers provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate scores
        results = OnboardingService.calculate_vak_scores(answers)
        
        # Save to onboarding progress
        OnboardingService.save_step_data(
            request.user,
            'style_assessment',
            {'vak_answers': answers}
        )
        
        return Response({
            'results': results,
            'explanation': OnboardingService._get_style_explanation(results['primary_style']),
        })
    
    @staticmethod
    def _get_style_explanation(style: str) -> str:
        """Get explanation for learning style."""
        explanations = {
            'visual': 'You learn best through images, diagrams, and visual representations. '
                      "We'll prioritize picture-based exercises and colorful content for you.",
            'auditory': 'You learn best through listening and verbal explanations. '
                        "We'll include more audio content and speaking exercises.",
            'kinesthetic': 'You learn best by doing and practicing. '
                           "We'll focus on interactive exercises and hands-on activities.",
        }
        return explanations.get(style, '')


# Add this to services.py as a static method
OnboardingService._get_style_explanation = SubmitVAKAssessmentView._get_style_explanation


class CompleteOnboardingView(APIView):
    """
    Complete the full onboarding and create learning profile.
    POST /api/v1/onboarding/complete/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            profile, summary = OnboardingService.complete_onboarding(request.user)
            
            return Response({
                'success': True,
                'message': 'Onboarding completed! Your learning journey begins.',
                'summary': summary,
                'next_step': 'world_map',  # Where to redirect after onboarding
            })
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class AvailableLanguagesView(APIView):
    """
    Get available languages for learning.
    GET /api/v1/onboarding/languages/
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Hardcoded for now, later from database
        languages = [
            {'code': 'en', 'name': 'English', 'native_name': 'English', 'flag': '🇺🇸'},
            {'code': 'es', 'name': 'Spanish', 'native_name': 'Español', 'flag': '🇪🇸'},
            {'code': 'de', 'name': 'German', 'native_name': 'Deutsch', 'flag': '🇩🇪'},
            {'code': 'fr', 'name': 'French', 'native_name': 'Français', 'flag': '🇫🇷'},
            {'code': 'pt', 'name': 'Portuguese', 'native_name': 'Português', 'flag': '🇧🇷'},
            {'code': 'it', 'name': 'Italian', 'native_name': 'Italiano', 'flag': '🇮🇹'},
            {'code': 'ja', 'name': 'Japanese', 'native_name': '日本語', 'flag': '🇯🇵'},
            {'code': 'zh', 'name': 'Chinese', 'native_name': '中文', 'flag': '🇨🇳'},
            {'code': 'ko', 'name': 'Korean', 'native_name': '한국어', 'flag': '🇰🇷'},
        ]
        
        return Response({
            'native_languages': languages,
            'target_languages': [l for l in languages if l['code'] == 'en'],  # Start with English only
        })


class OnboardingOptionsView(APIView):
    """
    Get available options for onboarding steps (goals, interests, work_domains).
    GET /api/v1/onboarding/options/
    
    Returns tags from database so frontend stays in sync.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        from apps.scenarios.models import Tag
        
        # Get all tags grouped by type
        def get_tags_by_type(tag_type):
            return [
                {
                    'id': tag.value,
                    'icon': tag.icon,
                    'label': tag.display_name,
                }
                for tag in Tag.objects.filter(type=tag_type).order_by('value')
            ]
        
        return Response({
            'goals': get_tags_by_type('goal'),
            'interests': get_tags_by_type('interest'),
            'domains': get_tags_by_type('domain'),
            'work_domains': get_tags_by_type('work_domain'),
            'skills': get_tags_by_type('skill'),
        })
