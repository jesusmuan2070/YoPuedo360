/**
 * VAK Step - Compact one question at a time
 */

import { useState } from 'react';

const QUESTIONS = [
    {
        q: '¿Cómo recuerdas mejor una palabra nueva?',
        options: [
            { id: 'visual', icon: '👁️', text: 'Viéndola escrita' },
            { id: 'auditory', icon: '👂', text: 'Escuchándola' },
            { id: 'kinesthetic', icon: '✋', text: 'Escribiéndola' },
        ]
    },
    {
        q: '¿Cómo prefieres estudiar?',
        options: [
            { id: 'visual', icon: '📊', text: 'Con diagramas' },
            { id: 'auditory', icon: '🎧', text: 'Con audios' },
            { id: 'kinesthetic', icon: '✍️', text: 'Practicando' },
        ]
    },
    {
        q: '¿Qué te ayuda más a entender?',
        options: [
            { id: 'visual', icon: '🎬', text: 'Videos/imágenes' },
            { id: 'auditory', icon: '🗣️', text: 'Explicaciones' },
            { id: 'kinesthetic', icon: '🎮', text: 'Ejercicios' },
        ]
    },
];

export default function VAKStep({ data, onComplete, onBack }) {
    const [current, setCurrent] = useState(0);
    const [answers, setAnswers] = useState([]);

    const handleAnswer = (answerId) => {
        const newAnswers = [...answers, answerId];
        setAnswers(newAnswers);

        if (current < QUESTIONS.length - 1) {
            setTimeout(() => setCurrent(c => c + 1), 200);
        } else {
            // Calculate result
            const counts = { visual: 0, auditory: 0, kinesthetic: 0 };
            newAnswers.forEach(a => counts[a]++);
            const primary = Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
            onComplete({
                vak_answers: newAnswers.map((a, i) => ({ question_order: i + 1, answer: a })),
                learning_style: primary
            });
        }
    };

    const q = QUESTIONS[current];

    return (
        <div>
            <h2 className="text-xl font-bold text-center text-gray-900 mb-1">🧠 Tu Estilo</h2>
            <p className="text-gray-500 text-sm text-center mb-4">Pregunta {current + 1} de {QUESTIONS.length}</p>

            {/* Progress dots */}
            <div className="flex justify-center gap-2 mb-4">
                {QUESTIONS.map((_, i) => (
                    <div
                        key={i}
                        className={`w-2 h-2 rounded-full transition-all ${i < current ? 'bg-green-500' : i === current ? 'bg-purple-600 scale-125' : 'bg-gray-300'
                            }`}
                    />
                ))}
            </div>

            {/* Question */}
            <div className="bg-gray-50 rounded-xl p-4 mb-4">
                <p className="text-center font-medium text-gray-800 text-sm">{q.q}</p>
            </div>

            {/* Options */}
            <div className="space-y-2 mb-4">
                {q.options.map(opt => (
                    <button
                        key={opt.id}
                        onClick={() => handleAnswer(opt.id)}
                        className="w-full flex items-center gap-3 p-3 bg-white border-2 border-gray-100 rounded-xl hover:border-purple-400 hover:bg-purple-50 transition-all text-left"
                    >
                        <span className="text-xl">{opt.icon}</span>
                        <span className="text-sm font-medium text-gray-700">{opt.text}</span>
                    </button>
                ))}
            </div>

            <button onClick={onBack} className="text-purple-600 font-medium text-sm">
                ← Atrás
            </button>
        </div>
    );
}
