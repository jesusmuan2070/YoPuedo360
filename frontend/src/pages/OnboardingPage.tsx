/**
 * Onboarding Page - Compact, no-scroll design
 * Updated with new steps for personalization
 */

import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { onboardingAPI } from '../services/api';

import WelcomeStep from '../components/onboarding/WelcomeStep';
import LanguageStep from '../components/onboarding/LanguageStep';
import GoalStep from '../components/onboarding/GoalStep';
import InterestsStep from '../components/onboarding/InterestsStep';
import ProfessionStep from '../components/onboarding/ProfessionStep';
import LevelStep from '../components/onboarding/LevelStep';
import VAKStep from '../components/onboarding/VAKStep';
import TimeStep from '../components/onboarding/TimeStep';
import SignUpStep from '../components/onboarding/SignUpStep';

const STEPS = [
    { id: 1, type: 'welcome', component: WelcomeStep },
    { id: 2, type: 'language_select', component: LanguageStep },
    { id: 3, type: 'goal_select', component: GoalStep },
    { id: 4, type: 'interests_select', component: InterestsStep },
    { id: 5, type: 'profession_select', component: ProfessionStep },
    { id: 6, type: 'level_select', component: LevelStep },
    { id: 7, type: 'style_assessment', component: VAKStep },
    { id: 8, type: 'time_commitment', component: TimeStep },
    { id: 9, type: 'signup', component: SignUpStep },
];

export default function OnboardingPage() {
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth();

    const [currentStep, setCurrentStep] = useState(1);
    const [collectedData, setCollectedData] = useState({});
    const [loading, setLoading] = useState(false);

    // Skip to world if already authenticated
    useEffect(() => {
        if (isAuthenticated) {
            navigate('/world');
        }
    }, [isAuthenticated, navigate]);

    const handleStepComplete = (data) => {
        setCollectedData(prev => ({ ...prev, ...data }));
        if (currentStep < STEPS.length) {
            setCurrentStep(prev => prev + 1);
        }
    };

    const handleBack = () => {
        if (currentStep > 1) {
            setCurrentStep(prev => prev - 1);
        }
    };

    const handleComplete = () => {
        navigate('/world');
    };

    const CurrentStepComponent = STEPS[currentStep - 1]?.component;
    const progress = (currentStep / STEPS.length) * 100;

    return (
        <div className="min-h-screen bg-gradient-to-br from-violet-600 via-purple-600 to-indigo-700 flex flex-col items-center justify-center p-4">
            {/* Progress bar */}
            <div className="w-full max-w-lg mb-4">
                <div className="flex justify-between items-center mb-2">
                    <Link to="/" className="text-white/70 hover:text-white text-sm">
                        ← Inicio
                    </Link>
                    <span className="text-white/70 text-sm">{currentStep}/{STEPS.length}</span>
                </div>
                <div className="h-1.5 bg-white/20 rounded-full overflow-hidden">
                    <div
                        className="h-full bg-white rounded-full transition-all duration-300"
                        style={{ width: `${progress}%` }}
                    />
                </div>
            </div>

            {/* Step card */}
            <div className="w-full max-w-lg">
                <div className="backdrop-blur-xl bg-white/95 rounded-3xl shadow-2xl p-8 border border-white/20">
                    {CurrentStepComponent && (
                        <CurrentStepComponent
                            data={collectedData}
                            onComplete={handleStepComplete}
                            onBack={handleBack}
                            onFinish={handleComplete}
                            loading={loading}
                            isFirstStep={currentStep === 1}
                            isLastStep={currentStep === STEPS.length}
                        />
                    )}
                </div>
            </div>
        </div>
    );
}
