/**
 * WorldMapPage - Main game interface showing scenarios
 * Uses Tailwind CSS
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { recommendationsAPI } from '../services/api';
import ScenarioCard from '../components/game/ScenarioCard';
import Header from '../components/layout/Header';

interface Scenario {
    id: number;
    slug: string;
    title: string;
    description: string;
    category: string;
    difficulty: string;
    estimated_minutes: number;
    milestones_count: number;
}

function WorldMapPage() {
    const navigate = useNavigate();
    const [scenarios, setScenarios] = useState<Scenario[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [showAriaBadge, setShowAriaBadge] = useState(true);

    // Auto-hide ARIA badge after 5 seconds
    useEffect(() => {
        const timer = setTimeout(() => setShowAriaBadge(false), 5000);
        return () => clearTimeout(timer);
    }, []);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);

            // Load recommended scenarios from ARIA
            const scenariosRes = await recommendationsAPI.getRecommended(12);
            setScenarios(scenariosRes.data.scenarios || []);

        } catch (err) {
            console.error('Error loading data:', err);
            setError('Error cargando datos. Por favor intenta de nuevo.');
        } finally {
            setLoading(false);
        }
    };

    const handleScenarioClick = (scenario: Scenario) => {
        navigate(`/scenario/${scenario.slug}`);
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-orange-100 via-amber-50 to-orange-50">
                <Header showStats={true} />
                <div className="flex flex-col items-center justify-center h-[calc(100vh-64px)]">
                    <div className="w-12 h-12 border-4 border-gray-200 border-t-[#667eea] rounded-full animate-spin mb-4"></div>
                    <p className="text-lg text-gray-600">Cargando tu mundo...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-orange-100 via-amber-50 to-orange-50">
                <Header showStats={true} />
                <div className="flex flex-col items-center justify-center h-[calc(100vh-64px)]">
                    <p className="text-lg mb-4 text-gray-700">{error}</p>
                    <button
                        onClick={loadData}
                        className="btn-primary px-8"
                    >
                        Reintentar
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-orange-100 via-amber-50 to-orange-50">
            {/* Header Component */}
            <Header showStats={true} />

            {/* Main Content */}
            <main className="p-6 max-w-7xl mx-auto">
                {/* Page Title */}
                <div className="mb-6">
                    <h1 className="text-2xl font-bold text-gray-800">
                        🏰 Tu Mundo
                    </h1>
                    <p className="text-gray-600 text-sm mt-1">
                        Explora escenarios personalizados para ti
                    </p>
                </div>

                {/* ARIA Badge - Shows for 5 seconds */}
                {showAriaBadge && (
                    <div className="inline-flex items-center gap-3 px-4 py-3 bg-gradient-to-r from-purple-500/20 to-cyan-500/20 border border-purple-500/40 rounded-full mb-6 animate-pulse">
                        <span className="text-xl">🤖</span>
                        <span className="text-sm text-gray-700">
                            ARIA ha seleccionado estos escenarios basándose en tu perfil
                        </span>
                    </div>
                )}

                {/* Scenarios Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                    {scenarios.map((scenario, index) => (
                        <ScenarioCard
                            key={scenario.id}
                            scenario={scenario}
                            rank={index + 1}
                            onClick={() => handleScenarioClick(scenario)}
                        />
                    ))}
                </div>

                {scenarios.length === 0 && (
                    <div className="text-center py-16 text-gray-500">
                        <p className="text-lg">No hay escenarios disponibles.</p>
                        <p>Completa tu perfil para recibir recomendaciones personalizadas.</p>
                    </div>
                )}
            </main>
        </div>
    );
}

export default WorldMapPage;
