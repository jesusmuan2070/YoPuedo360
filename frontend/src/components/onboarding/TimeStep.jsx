/**
 * Time Step - Compact design
 */

import { useState } from 'react';

const TIMES = [
    { value: 5, icon: '⚡', label: '5 min', desc: 'Casual' },
    { value: 15, icon: '🔥', label: '15 min', desc: 'Regular', rec: true },
    { value: 30, icon: '💪', label: '30 min', desc: 'Serio' },
    { value: 60, icon: '🚀', label: '60 min', desc: 'Intensivo' },
];

export default function TimeStep({ data, onComplete, onBack }) {
    const [time, setTime] = useState(data.daily_goal_minutes || 15);

    return (
        <div>
            <h2 className="text-xl font-bold text-center text-gray-900 mb-1">⏰ Tu Meta Diaria</h2>
            <p className="text-gray-500 text-sm text-center mb-5">¿Cuánto tiempo puedes dedicar?</p>

            <div className="grid grid-cols-2 gap-2 mb-4">
                {TIMES.map(t => (
                    <button
                        key={t.value}
                        onClick={() => setTime(t.value)}
                        className={`relative flex flex-col items-center p-4 rounded-xl transition-all ${time === t.value
                                ? 'bg-purple-100 ring-2 ring-purple-500'
                                : 'bg-gray-50 hover:bg-gray-100'
                            }`}
                    >
                        {t.rec && (
                            <span className="absolute -top-2 bg-purple-600 text-white text-[10px] px-2 py-0.5 rounded-full">
                                Recomendado
                            </span>
                        )}
                        <span className="text-2xl mb-1">{t.icon}</span>
                        <span className="font-bold text-gray-900">{t.label}</span>
                        <span className="text-xs text-gray-500">{t.desc}</span>
                    </button>
                ))}
            </div>

            <div className="bg-yellow-50 rounded-xl p-3 mb-4">
                <p className="text-xs text-yellow-700 text-center">
                    💡 La constancia es más importante que la duración
                </p>
            </div>

            <div className="flex gap-3">
                <button onClick={onBack} className="px-4 py-2.5 text-purple-600 font-medium">
                    ← Atrás
                </button>
                <button
                    onClick={() => onComplete({ daily_goal_minutes: time })}
                    className="flex-1 py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl"
                >
                    Continuar
                </button>
            </div>
        </div>
    );
}
