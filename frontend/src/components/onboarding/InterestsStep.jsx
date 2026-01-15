/**
 * Interests Step - Select personal interests for content personalization
 * Loads options from backend API
 */

import { useState, useEffect } from 'react';
import { onboardingAPI } from '../../services/api';

export default function InterestsStep({ data, onComplete, onBack }) {
    const [interests, setInterests] = useState([]);
    const [selectedInterests, setSelectedInterests] = useState(data.interests || {});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadOptions() {
            try {
                const response = await onboardingAPI.getOptions();
                // Only use interests from backend
                setInterests(response.data.interests || []);
            } catch (error) {
                console.error('Error loading interests:', error);
                setInterests([]);
            } finally {
                setLoading(false);
            }
        }
        loadOptions();
    }, []);

    const MAX_INTERESTS = 5;

    const toggleInterest = (interestId) => {
        setSelectedInterests(prev => {
            const newInterests = { ...prev };
            if (newInterests[interestId]) {
                delete newInterests[interestId];
            } else {
                // Check max limit
                if (Object.keys(newInterests).length >= MAX_INTERESTS) {
                    return prev;
                }
                // No weights - all interests equal (stored as true)
                newInterests[interestId] = true;
            }
            return newInterests;
        });
    };

    const hasSelection = Object.keys(selectedInterests).length > 0;
    const isMaxReached = Object.keys(selectedInterests).length >= MAX_INTERESTS;

    if (loading) {
        return (
            <div className="flex justify-center items-center py-10">
                <div className="animate-spin w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full" />
            </div>
        );
    }

    return (
        <div>
            <h2 className="text-xl font-bold text-center text-gray-900 mb-1">🎯 Tus Intereses</h2>
            <p className="text-gray-500 text-sm text-center mb-4">
                ¿Qué te gusta? Personalizaremos tu contenido
            </p>

            <div className="grid grid-cols-3 gap-3 mb-5">
                {interests.map(interest => {
                    const isSelected = selectedInterests[interest.id] !== undefined;
                    return (
                        <button
                            key={interest.id}
                            onClick={() => toggleInterest(interest.id)}
                            className={`flex flex-col items-center p-3 rounded-xl transition-all ${isSelected
                                ? 'bg-purple-100 ring-2 ring-purple-500 scale-105'
                                : 'bg-gray-50 hover:bg-gray-100'
                                }`}
                        >
                            <span className="text-2xl mb-1">{interest.icon}</span>
                            <span className="text-xs text-gray-700 text-center leading-tight">{interest.label}</span>
                        </button>
                    );
                })}
            </div>

            <p className={`text-center text-sm mb-4 ${isMaxReached ? 'text-orange-600 font-medium' : 'text-purple-600'}`}>
                {Object.keys(selectedInterests).length}/{MAX_INTERESTS} seleccionados
                {isMaxReached && ' (máximo alcanzado)'}
            </p>

            <div className="flex gap-3">
                <button onClick={onBack} className="px-4 py-2.5 text-purple-600 font-medium">
                    ← Atrás
                </button>
                <button
                    onClick={() => onComplete({ interests: selectedInterests })}
                    disabled={!hasSelection}
                    className="flex-1 py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl disabled:opacity-50"
                >
                    Continuar
                </button>
            </div>
        </div>
    );
}
