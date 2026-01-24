/**
 * Level Step - Compact design
 */

import { useState } from 'react';

const LEVELS = [
    { value: 1, icon: '🌱', label: 'Principiante', desc: 'Empezando desde cero' },
    { value: 2, icon: '🌿', label: 'Básico', desc: 'Conozco algunas palabras' },
    { value: 3, icon: '🌳', label: 'Intermedio', desc: 'Puedo conversar' },
    { value: 4, icon: '🌲', label: 'Avanzado', desc: 'Domino el idioma' },
];

export default function LevelStep({ data, onComplete, onBack }) {
    const [level, setLevel] = useState(data.initial_level || null);

    return (
        <div>
            <h2 className="text-xl font-bold text-center text-gray-900 mb-1">📊 Tu Nivel</h2>
            <p className="text-gray-500 text-sm text-center mb-5">¿Cuánto sabes del idioma?</p>

            <div className="space-y-2 mb-6">
                {LEVELS.map(l => (
                    <button
                        key={l.value}
                        onClick={() => setLevel(l.value)}
                        className={`w-full flex items-center gap-3 p-3 rounded-xl transition-all text-left ${level === l.value
                                ? 'bg-purple-100 ring-2 ring-purple-500'
                                : 'bg-gray-50 hover:bg-gray-100'
                            }`}
                    >
                        <span className="text-2xl">{l.icon}</span>
                        <div className="flex-1">
                            <p className="font-semibold text-gray-900 text-sm">{l.label}</p>
                            <p className="text-xs text-gray-500">{l.desc}</p>
                        </div>
                        {level === l.value && <span className="text-purple-600">✓</span>}
                    </button>
                ))}
            </div>

            <div className="flex gap-3">
                <button onClick={onBack} className="px-4 py-2.5 text-purple-600 font-medium">
                    ← Atrás
                </button>
                <button
                    onClick={() => onComplete({ initial_level: level })}
                    disabled={!level}
                    className="flex-1 py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl disabled:opacity-50"
                >
                    Continuar
                </button>
            </div>
        </div>
    );
}
