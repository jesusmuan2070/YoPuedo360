/**
 * SignUp Step - Final step, create account
 */

import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { onboardingAPI } from '../../services/api';

export default function SignUpStep({ data, onComplete, onBack, onFinish }) {
    const { register } = useAuth();
    const [formData, setFormData] = useState({ email: '', username: '', password: '' });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
        setError('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (formData.password.length < 8) {
            setError('Mínimo 8 caracteres en la contraseña');
            return;
        }

        setLoading(true);
        try {
            const result = await register(formData.email, formData.username, formData.password);

            if (result.success) {
                // Save all onboarding steps to backend
                try {
                    // Send each step's data
                    if (data.native_language || data.target_language) {
                        await onboardingAPI.completeStep('language_select', {
                            native_language: data.native_language || 'es',
                            target_language: data.target_language || 'en',
                        });
                    }

                    if (data.goals) {
                        await onboardingAPI.completeStep('goal_select', { goals: data.goals });
                    }

                    if (data.interests) {
                        await onboardingAPI.completeStep('interests_select', { interests: data.interests });
                    }

                    if (data.work_domain || data.profession) {
                        await onboardingAPI.completeStep('profession_select', {
                            work_domain: data.work_domain || '',
                            profession: data.profession || '',
                            hobbies: data.hobbies || [],
                        });
                    }

                    if (data.initial_level) {
                        await onboardingAPI.completeStep('level_select', { initial_level: data.initial_level });
                    }

                    if (data.vak_answers) {
                        await onboardingAPI.completeStep('style_assessment', { vak_answers: data.vak_answers });
                    }

                    if (data.daily_goal_minutes) {
                        await onboardingAPI.completeStep('time_commitment', { daily_goal_minutes: data.daily_goal_minutes });
                    }

                    // Complete onboarding and create LearningProfile
                    await onboardingAPI.complete();

                    console.log('✅ Onboarding data saved successfully');
                } catch (saveError) {
                    console.error('Error saving onboarding data:', saveError);
                    // Continue anyway - user is registered
                }

                onFinish();
            } else {
                setError(result.error?.email?.[0] || result.error?.username?.[0] || 'Error al registrar');
            }
        } catch (err) {
            setError('Error de conexión');
        }
        setLoading(false);
    };

    return (
        <div>
            <div className="text-center mb-4">
                <div className="w-14 h-14 bg-gradient-to-br from-green-400 to-emerald-500 rounded-2xl flex items-center justify-center mx-auto mb-3">
                    <span className="text-2xl">🎉</span>
                </div>
                <h2 className="text-xl font-bold text-gray-900">¡Último paso!</h2>
                <p className="text-gray-500 text-sm">Crea tu cuenta para guardar tu progreso</p>
            </div>

            {/* Summary */}
            <div className="bg-gray-50 rounded-xl p-3 mb-4 text-xs">
                <div className="flex justify-between mb-1">
                    <span className="text-gray-500">Idioma:</span>
                    <span className="font-medium">🇺🇸 English</span>
                </div>
                <div className="flex justify-between mb-1">
                    <span className="text-gray-500">Meta:</span>
                    <span className="font-medium capitalize">{data.learning_goal || 'General'}</span>
                </div>
                <div className="flex justify-between">
                    <span className="text-gray-500">Tiempo diario:</span>
                    <span className="font-medium">{data.daily_goal_minutes || 15} min</span>
                </div>
            </div>

            {error && (
                <div className="bg-red-50 text-red-600 text-xs px-3 py-2 rounded-xl mb-3 text-center">
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-3">
                <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Email"
                    required
                    className="w-full px-3 py-2.5 bg-gray-50 rounded-xl text-sm focus:ring-2 focus:ring-purple-500 outline-none"
                />
                <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    placeholder="Usuario"
                    required
                    className="w-full px-3 py-2.5 bg-gray-50 rounded-xl text-sm focus:ring-2 focus:ring-purple-500 outline-none"
                />
                <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Contraseña (mín. 8 caracteres)"
                    required
                    className="w-full px-3 py-2.5 bg-gray-50 rounded-xl text-sm focus:ring-2 focus:ring-purple-500 outline-none"
                />

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl disabled:opacity-50"
                >
                    {loading ? '⏳ Creando...' : 'Crear cuenta y comenzar 🚀'}
                </button>
            </form>

            <button onClick={onBack} className="w-full text-purple-600 font-medium text-sm mt-3">
                ← Atrás
            </button>
        </div>
    );
}
