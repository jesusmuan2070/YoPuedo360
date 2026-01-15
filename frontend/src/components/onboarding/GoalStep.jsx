/**
 * Goal Step - Multi-select with weights
 * Loads options from backend API
 */

import { useState, useEffect } from 'react';
import { onboardingAPI } from '../../services/api';

export default function GoalStep({ data, onComplete, onBack }) {
    const [goals, setGoals] = useState([]);
    const [selectedGoals, setSelectedGoals] = useState(data.goals || {});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadOptions() {
            try {
                const response = await onboardingAPI.getOptions();
                setGoals(response.data.goals || []);
            } catch (error) {
                console.error('Error loading goals:', error);
                setGoals([]);
            } finally {
                setLoading(false);
            }
        }
        loadOptions();
    }, []);

    const MAX_GOALS = 2;

    const toggleGoal = (goalId) => {
        setSelectedGoals(prev => {
            const newGoals = { ...prev };
            if (newGoals[goalId]) {
                // Deselecting
                delete newGoals[goalId];
                // If one remains, give it 100%
                const remaining = Object.keys(newGoals);
                if (remaining.length === 1) {
                    newGoals[remaining[0]] = 1.0;
                }
            } else {
                // Check max limit
                if (Object.keys(newGoals).length >= MAX_GOALS) {
                    return prev;
                }
                const numSelected = Object.keys(newGoals).length;
                if (numSelected === 0) {
                    // First selection = 100%
                    newGoals[goalId] = 1.0;
                } else {
                    // Second selection: first becomes 70%, second 30%
                    const firstGoal = Object.keys(newGoals)[0];
                    newGoals[firstGoal] = 0.7;
                    newGoals[goalId] = 0.3;
                }
            }
            return newGoals;
        });
    };

    const hasSelection = Object.keys(selectedGoals).length > 0;
    const isMaxReached = Object.keys(selectedGoals).length >= MAX_GOALS;

    if (loading) {
        return (
            <div className="flex justify-center items-center py-10">
                <div className="animate-spin w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full" />
            </div>
        );
    }

    return (
        <div>
            <h2 className="text-xl font-bold text-center text-gray-900 mb-1">🎯 Tus Metas</h2>
            <p className="text-gray-500 text-sm text-center mb-5">Selecciona hasta 2 metas</p>

            <div className="grid grid-cols-2 gap-3 mb-4">
                {goals.map(g => {
                    const isSelected = selectedGoals[g.id] !== undefined;
                    const weight = selectedGoals[g.id];
                    return (
                        <button
                            key={g.id}
                            onClick={() => toggleGoal(g.id)}
                            className={`flex items-center gap-3 px-4 py-3 rounded-xl border-2 transition-all ${isSelected
                                ? 'bg-purple-50 border-purple-500 shadow-md'
                                : isMaxReached
                                    ? 'bg-gray-100 border-gray-200 opacity-50'
                                    : 'bg-white border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                                }`}
                        >
                            <span className="text-2xl">{g.icon}</span>
                            <span className={`text-sm font-medium text-left flex-1 ${isSelected ? 'text-purple-700' : 'text-gray-700'}`}>
                                {g.label}
                            </span>
                            {isSelected && (
                                <span className="text-xs font-bold text-purple-600 bg-purple-100 px-2 py-0.5 rounded-full">
                                    {Math.round(weight * 100)}%
                                </span>
                            )}
                        </button>
                    );
                })}
            </div>

            <p className={`text-center text-sm mb-4 ${isMaxReached ? 'text-green-600 font-medium' : 'text-gray-500'}`}>
                {Object.keys(selectedGoals).length}/{MAX_GOALS} seleccionadas
            </p>

            <div className="flex gap-3">
                <button onClick={onBack} className="px-4 py-2.5 text-purple-600 font-medium">
                    ← Atrás
                </button>
                <button
                    onClick={() => onComplete({ goals: selectedGoals })}
                    disabled={!hasSelection}
                    className="flex-1 py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl disabled:opacity-50"
                >
                    Continuar
                </button>
            </div>
        </div>
    );
}
