/**
 * Profession Step - Capture profession and hobbies for AI personalization
 * Loads work_domains from backend API
 */

import { useState, useEffect } from 'react';
import { onboardingAPI } from '../../services/api';

export default function ProfessionStep({ data, onComplete, onBack }) {
    const [workDomains, setWorkDomains] = useState([]);
    const [workDomain, setWorkDomain] = useState(data.work_domain || '');
    const [profession, setProfession] = useState(data.profession || '');
    const [hobbiesText, setHobbiesText] = useState(
        data.hobbies ? data.hobbies.join(', ') : ''
    );
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadOptions() {
            try {
                const response = await onboardingAPI.getOptions();
                setWorkDomains(response.data.work_domains || []);
            } catch (error) {
                console.error('Error loading work domains:', error);
                setWorkDomains([]);
            } finally {
                setLoading(false);
            }
        }
        loadOptions();
    }, []);

    const handleContinue = () => {
        const hobbies = hobbiesText
            .split(',')
            .map(h => h.trim())
            .filter(h => h.length > 0);

        onComplete({
            work_domain: workDomain,
            profession: profession,
            hobbies: hobbies,
        });
    };

    const isValid = workDomain && profession.length >= 3;

    if (loading) {
        return (
            <div className="flex justify-center items-center py-10">
                <div className="animate-spin w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full" />
            </div>
        );
    }

    return (
        <div>
            <h2 className="text-xl font-bold text-center text-gray-900 mb-1">💼 Tu Perfil</h2>
            <p className="text-gray-500 text-sm text-center mb-4">
                Personalizaremos el contenido para ti
            </p>

            {/* Work Domain */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    Área de trabajo
                </label>
                <div className="grid grid-cols-4 gap-2">
                    {workDomains.map(domain => (
                        <button
                            key={domain.id}
                            onClick={() => setWorkDomain(domain.id)}
                            className={`flex flex-col items-center p-2 rounded-lg transition-all text-xs ${workDomain === domain.id
                                ? 'bg-purple-100 ring-2 ring-purple-500'
                                : 'bg-gray-50 hover:bg-gray-100'
                                }`}
                        >
                            <span className="text-lg">{domain.icon}</span>
                            <span className="text-gray-700 mt-1">{domain.label}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Profession */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    ¿A qué te dedicas? (específico)
                </label>
                <input
                    type="text"
                    value={profession}
                    onChange={(e) => setProfession(e.target.value)}
                    placeholder="Ej: Desarrollador web, Enfermera, Chef..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
                />
            </div>

            {/* Hobbies */}
            <div className="mb-5">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Hobbies/Deportes (separados por coma)
                </label>
                <input
                    type="text"
                    value={hobbiesText}
                    onChange={(e) => setHobbiesText(e.target.value)}
                    placeholder="Ej: nadar, soccer, leer, videojuegos..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
                />
            </div>

            <div className="flex gap-3">
                <button onClick={onBack} className="px-4 py-2.5 text-purple-600 font-medium">
                    ← Atrás
                </button>
                <button
                    onClick={handleContinue}
                    disabled={!isValid}
                    className="flex-1 py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl disabled:opacity-50"
                >
                    Continuar
                </button>
            </div>
        </div>
    );
}
