/**
 * Language Step - Compact design
 */

import { useState } from 'react';

const LANGUAGES = [
    { code: 'es', flag: '🇪🇸', name: 'Español' },
    { code: 'en', flag: '🇺🇸', name: 'English' },
    { code: 'pt', flag: '🇧🇷', name: 'Português' },
    { code: 'fr', flag: '🇫🇷', name: 'Français' },
    { code: 'de', flag: '🇩🇪', name: 'Deutsch' },
    { code: 'it', flag: '🇮🇹', name: 'Italiano' },
];

export default function LanguageStep({ data, onComplete, onBack }) {
    const [native, setNative] = useState(data.native_language || 'es');
    const [target, setTarget] = useState(data.target_language || 'en');

    return (
        <div>
            <h2 className="text-xl font-bold text-center text-gray-900 mb-1">🌍 Idiomas</h2>
            <p className="text-gray-500 text-sm text-center mb-5">¿Qué idioma quieres aprender?</p>

            {/* Native */}
            <label className="text-xs font-semibold text-gray-500 uppercase mb-2 block">Hablo</label>
            <div className="grid grid-cols-6 gap-2 mb-4">
                {LANGUAGES.map(lang => (
                    <button
                        key={`n-${lang.code}`}
                        onClick={() => setNative(lang.code)}
                        className={`p-2 rounded-xl text-2xl transition-all ${native === lang.code
                                ? 'bg-purple-100 ring-2 ring-purple-500 scale-110'
                                : 'bg-gray-50 hover:bg-gray-100'
                            }`}
                    >
                        {lang.flag}
                    </button>
                ))}
            </div>

            {/* Target */}
            <label className="text-xs font-semibold text-gray-500 uppercase mb-2 block">Quiero aprender</label>
            <button
                onClick={() => setTarget('en')}
                className={`w-full flex items-center gap-3 p-3 rounded-xl transition-all mb-5 ${target === 'en'
                        ? 'bg-purple-100 ring-2 ring-purple-500'
                        : 'bg-gray-50 hover:bg-gray-100'
                    }`}
            >
                <span className="text-3xl">🇺🇸</span>
                <span className="font-semibold text-gray-900">English</span>
                <span className="ml-auto bg-purple-600 text-white text-xs px-2 py-1 rounded-full">Popular</span>
            </button>

            {/* Buttons */}
            <div className="flex gap-3">
                <button onClick={onBack} className="px-4 py-2.5 text-purple-600 font-medium">
                    ← Atrás
                </button>
                <button
                    onClick={() => onComplete({ native_language: native, target_language: target })}
                    className="flex-1 py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl"
                >
                    Continuar
                </button>
            </div>
        </div>
    );
}
