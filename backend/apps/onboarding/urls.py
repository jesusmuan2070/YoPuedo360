"""
URL routes for onboarding API.
"""

from django.urls import path
from .views import (
    RegisterView,
    OnboardingStepsView,
    OnboardingProgressView,
    CompleteStepView,
    VAKAssessmentView,
    SubmitVAKAssessmentView,
    CompleteOnboardingView,
    AvailableLanguagesView,
    OnboardingOptionsView,
)

urlpatterns = [
    # Registration
    path('register/', RegisterView.as_view(), name='register'),
    
    # Onboarding flow
    path('steps/', OnboardingStepsView.as_view(), name='onboarding-steps'),
    path('progress/', OnboardingProgressView.as_view(), name='onboarding-progress'),
    path('complete-step/', CompleteStepView.as_view(), name='complete-step'),
    path('complete/', CompleteOnboardingView.as_view(), name='complete-onboarding'),
    
    # VAK Assessment
    path('vak-assessment/', VAKAssessmentView.as_view(), name='vak-assessment'),
    path('submit-vak/', SubmitVAKAssessmentView.as_view(), name='submit-vak'),
    
    # Helper endpoints
    path('languages/', AvailableLanguagesView.as_view(), name='available-languages'),
    path('options/', OnboardingOptionsView.as_view(), name='onboarding-options'),
]
