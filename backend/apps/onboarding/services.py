"""
Onboarding service layer.
Handles business logic for onboarding flow and VAK assessment calculation.
"""

from typing import Dict, List, Tuple, Optional
from django.utils import timezone
from apps.users.models import User, LearningProfile
from .models import UserOnboardingProgress, VAKAssessmentQuestion


class OnboardingService:
    """
    Service class for handling onboarding logic.
    """
    
    @staticmethod
    def calculate_vak_scores(answers: List[Dict]) -> Dict:
        """
        Calculate VAK scores from user's assessment answers.
        
        Args:
            answers: List of {'question_order': int, 'answer': 'visual'|'auditory'|'kinesthetic'}
        
        Returns:
            Dict with scores and primary/secondary style
        """
        scores = {
            'visual': 0,
            'auditory': 0,
            'kinesthetic': 0,
        }
        
        for answer in answers:
            channel = answer.get('answer')
            if channel in scores:
                scores[channel] += 1
        
        # Convert to percentages
        total = len(answers) if answers else 1
        percentages = {
            'visual_score': round((scores['visual'] / total) * 100),
            'auditory_score': round((scores['auditory'] / total) * 100),
            'kinesthetic_score': round((scores['kinesthetic'] / total) * 100),
        }
        
        # Determine primary and secondary styles
        sorted_styles = sorted(
            [
                ('visual', percentages['visual_score']),
                ('auditory', percentages['auditory_score']),
                ('kinesthetic', percentages['kinesthetic_score']),
            ],
            key=lambda x: x[1],
            reverse=True
        )
        
        percentages['primary_style'] = sorted_styles[0][0]
        percentages['secondary_style'] = sorted_styles[1][0] if sorted_styles[1][1] > 20 else None
        
        return percentages
    
    @staticmethod
    def create_learning_profile(user: User, onboarding_data: Dict) -> LearningProfile:
        """
        Create learning profile from completed onboarding data.
        
        Args:
            user: The user object
            onboarding_data: Complete collected data from onboarding
        
        Returns:
            Created LearningProfile instance
        """
        # Calculate VAK scores
        vak_answers = onboarding_data.get('vak_answers', [])
        vak_results = OnboardingService.calculate_vak_scores(vak_answers)
        
        # Map initial_level to CEFR level
        initial_level = onboarding_data.get('initial_level', 1)
        cefr_map = {1: 'A1', 2: 'A2', 3: 'B1', 4: 'B2', 5: 'C1', 6: 'C2'}
        cefr_level = cefr_map.get(initial_level, 'A1')
        
        profile, created = LearningProfile.objects.update_or_create(
            user=user,
            defaults={
                # Language settings
                'native_language': onboarding_data.get('native_language', 'es'),
                'target_language': onboarding_data.get('target_language', 'en'),
                
                # Goals & Interests (NEW)
                'learning_goal': list(onboarding_data.get('goals', {}).keys())[0] if onboarding_data.get('goals') else 'general',
                'goals': onboarding_data.get('goals', {}),
                'interests': onboarding_data.get('interests', {}),
                
                # Profession & Hobbies (NEW)
                'work_domain': onboarding_data.get('work_domain', ''),
                'profession': onboarding_data.get('profession', ''),
                'hobbies': onboarding_data.get('hobbies', []),
                
                # Level & Time
                'daily_goal_minutes': onboarding_data.get('daily_goal_minutes', 15),
                'current_level': initial_level,
                'cefr_level': cefr_level,
                
                # VAK Assessment
                'visual_score': vak_results['visual_score'],
                'auditory_score': vak_results['auditory_score'],
                'kinesthetic_score': vak_results['kinesthetic_score'],
                'primary_style': vak_results['primary_style'],
                
                # Status
                'onboarding_completed': True,
            }
        )
        
        return profile
    
    @staticmethod
    def complete_onboarding(user: User) -> Tuple[LearningProfile, Dict]:
        """
        Complete the onboarding process for a user.
        Creates learning profile from collected data.
        
        Returns:
            Tuple of (LearningProfile, summary dict)
        """
        try:
            progress = UserOnboardingProgress.objects.get(user=user)
        except UserOnboardingProgress.DoesNotExist:
            raise ValueError("User has no onboarding progress")
        
        if progress.is_completed:
            raise ValueError("Onboarding already completed")
        
        # Create learning profile from collected data
        profile = OnboardingService.create_learning_profile(
            user, 
            progress.collected_data
        )
        
        # Mark onboarding as completed
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        
        # Calculate VAK results for summary
        vak_results = OnboardingService.calculate_vak_scores(
            progress.collected_data.get('vak_answers', [])
        )
        
        return profile, {
            'learning_profile_created': True,
            'native_language': profile.native_language,
            'target_language': profile.target_language,
            'primary_style': vak_results['primary_style'],
            'daily_goal': profile.daily_goal_minutes,
            'starting_level': profile.current_level,
        }
    
    @staticmethod
    def save_step_data(user: User, step_type: str, data: Dict) -> UserOnboardingProgress:
        """
        Save data from a completed onboarding step.
        
        Args:
            user: The user
            step_type: Type of step completed
            data: Data collected in this step
        
        Returns:
            Updated UserOnboardingProgress
        """
        progress, created = UserOnboardingProgress.objects.get_or_create(user=user)
        
        # Merge new data into collected_data
        collected = progress.collected_data or {}
        
        if step_type == 'language_select':
            collected['native_language'] = data.get('native_language')
            collected['target_language'] = data.get('target_language')
        elif step_type == 'goal_select':
            # Goals: max 2, with weights 70/30
            goals = data.get('goals', {})
            MAX_GOALS = 2
            
            # Limit to max 2 goals
            if len(goals) > MAX_GOALS:
                goals = dict(list(goals.items())[:MAX_GOALS])
            
            # Auto-assign weights: 1 goal = 100%, 2 goals = 70%/30%
            goal_list = list(goals.keys())
            if len(goal_list) == 1:
                goals = {goal_list[0]: 1.0}
            elif len(goal_list) >= 2:
                goals = {goal_list[0]: 0.7, goal_list[1]: 0.3}
            
            collected['goals'] = goals
            collected['learning_goal'] = goal_list[0] if goal_list else None
        elif step_type == 'interests_select':
            # Interests: max 5, all with equal weight
            interests = data.get('interests', {})
            MAX_INTERESTS = 5
            if len(interests) > MAX_INTERESTS:
                interests = dict(list(interests.items())[:MAX_INTERESTS])
            
            # Normalize to equal weight (sum = 1.0)
            num_interests = len(interests)
            if num_interests > 0:
                equal_weight = round(1.0 / num_interests, 2)
                interests = {k: equal_weight for k in interests.keys()}
            
            collected['interests'] = interests
        elif step_type == 'profession_select':
            # NEW: profession and hobbies
            collected['work_domain'] = data.get('work_domain', '')
            collected['profession'] = data.get('profession', '')
            collected['hobbies'] = data.get('hobbies', [])
        elif step_type == 'level_select':
            collected['initial_level'] = data.get('initial_level')
        elif step_type == 'time_commitment':
            collected['daily_goal_minutes'] = data.get('daily_goal_minutes')
        elif step_type == 'style_assessment':
            collected['vak_answers'] = data.get('vak_answers', [])
        elif step_type == 'avatar_create':
            collected['avatar_name'] = data.get('avatar_name')
        
        progress.collected_data = collected
        
        # Track completed steps
        completed = progress.completed_steps or []
        if step_type not in completed:
            completed.append(step_type)
        progress.completed_steps = completed
        
        # Advance current step
        progress.current_step += 1
        progress.save()
        
        return progress
    
    @staticmethod
    def get_user_progress(user: User) -> Optional[UserOnboardingProgress]:
        """Get user's onboarding progress."""
        try:
            return UserOnboardingProgress.objects.get(user=user)
        except UserOnboardingProgress.DoesNotExist:
            return None
    
    @staticmethod
    def get_default_vak_questions() -> List[Dict]:
        """
        Get default VAK assessment questions.
        Returns questions in format ready for frontend.
        """
        questions = VAKAssessmentQuestion.objects.filter(is_active=True).order_by('order')
        
        if not questions.exists():
            # Return hardcoded defaults if none in database
            return OnboardingService._get_hardcoded_vak_questions()
        
        return [
            {
                'order': q.order,
                'question_text': q.question_text,
                'options': [
                    {'id': 'visual', 'text': q.visual_option},
                    {'id': 'auditory', 'text': q.auditory_option},
                    {'id': 'kinesthetic', 'text': q.kinesthetic_option},
                ]
            }
            for q in questions
        ]
    
    @staticmethod
    def _get_hardcoded_vak_questions() -> List[Dict]:
        """Default VAK questions if none in database."""
        return [
            {
                'order': 1,
                'question_text': 'When learning a new word, what helps you remember it best?',
                'options': [
                    {'id': 'visual', 'text': 'Seeing it written down with images'},
                    {'id': 'auditory', 'text': 'Hearing it pronounced several times'},
                    {'id': 'kinesthetic', 'text': 'Writing it multiple times yourself'},
                ]
            },
            {
                'order': 2,
                'question_text': 'How do you prefer to follow directions to a new place?',
                'options': [
                    {'id': 'visual', 'text': 'Looking at a map or GPS with visual route'},
                    {'id': 'auditory', 'text': 'Listening to someone explain the route'},
                    {'id': 'kinesthetic', 'text': 'Walking/driving there once to learn'},
                ]
            },
            {
                'order': 3,
                'question_text': 'When studying, what environment do you prefer?',
                'options': [
                    {'id': 'visual', 'text': 'Clean space with charts and diagrams visible'},
                    {'id': 'auditory', 'text': 'Quiet place where I can read aloud or listen'},
                    {'id': 'kinesthetic', 'text': 'Active environment where I can move around'},
                ]
            },
            {
                'order': 4,
                'question_text': 'How do you best understand a new concept?',
                'options': [
                    {'id': 'visual', 'text': 'Seeing diagrams, charts, or demonstrations'},
                    {'id': 'auditory', 'text': 'Having someone explain it to me verbally'},
                    {'id': 'kinesthetic', 'text': 'Trying it myself through practice'},
                ]
            },
            {
                'order': 5,
                'question_text': 'When recalling a past experience, you tend to:',
                'options': [
                    {'id': 'visual', 'text': 'Picture it vividly in your mind'},
                    {'id': 'auditory', 'text': 'Remember sounds, voices, or conversations'},
                    {'id': 'kinesthetic', 'text': 'Remember feelings and physical sensations'},
                ]
            },
        ]
