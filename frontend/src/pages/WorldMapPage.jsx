/**
 * WorldMapPage - Main game interface showing scenarios
 * Uses Tailwind CSS
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { recommendationsAPI, progressAPI } from '../services/api';
import ScenarioCard from '../components/game/ScenarioCard';

function WorldMapPage() {
    const navigate = useNavigate();
    const [scenarios, setScenarios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [userProgress, setUserProgress] = useState(null);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);

            // Load recommended scenarios from ARIA
            const scenariosRes = await recommendationsAPI.getRecommended(12);
            setScenarios(scenariosRes.data.scenarios || []);

            // Load user progress
            try {
                const progressRes = await progressAPI.getMyProgress();
                setUserProgress(progressRes.data);
            } catch (e) {
                console.log('Progress not available yet');
            }

        } catch (err) {
            console.error('Error loading data:', err);
            setError('Error cargando datos. Por favor intenta de nuevo.');
        } finally {
            setLoading(false);
        }
    };

    const handleScenarioClick = (scenario) => {
        navigate(`/scenario/${scenario.slug}`);
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col items-center justify-center text-white">
                <div className="w-12 h-12 border-4 border-white/20 border-t-cyan-400 rounded-full animate-spin mb-4"></div>
                <p className="text-lg opacity-80">Cargando tu mundo...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col items-center justify-center text-white">
                <p className="text-lg mb-4">{error}</p>
                <button
                    onClick={loadData}
                    className="btn-primary px-8"
                >
                    Reintentar
                </button>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            {/* Header */}
            <header className="flex justify-between items-center p-6 bg-black/30 backdrop-blur-lg border-b border-white/10">
                <div>
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent">
                        🏰 Tu Mundo
                    </h1>
                    <p className="text-white/60 text-sm mt-1">
                        Explora escenarios personalizados para ti
                    </p>
                </div>
                <div className="flex gap-4">
                    {userProgress && (
                        <>
                            <div className="text-center px-4 py-2 bg-white/10 rounded-xl border border-white/10">
                                <span className="block text-xl font-bold text-emerald-400">
                                    {userProgress.summary?.milestones_completed || 0}
                                </span>
                                <span className="text-xs text-white/50 uppercase tracking-wide">
                                    Completados
                                </span>
                            </div>
                            <div className="text-center px-4 py-2 bg-white/10 rounded-xl border border-white/10">
                                <span className="block text-xl font-bold text-cyan-400">
                                    {userProgress.summary?.total_xp || 0}
                                </span>
                                <span className="text-xs text-white/50 uppercase tracking-wide">
                                    XP
                                </span>
                            </div>
                        </>
                    )}
                </div>
            </header>

            {/* Main Content */}
            <main className="p-6 max-w-7xl mx-auto">
                {/* ARIA Badge */}
                <div className="inline-flex items-center gap-3 px-4 py-3 bg-gradient-to-r from-purple-500/20 to-cyan-500/20 border border-purple-500/40 rounded-full mb-6">
                    <span className="text-xl">🤖</span>
                    <span className="text-sm text-white/90">
                        ARIA ha seleccionado estos escenarios basándose en tu perfil
                    </span>
                </div>

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
                    <div className="text-center py-16 text-white/60">
                        <p className="text-lg">No hay escenarios disponibles.</p>
                        <p>Completa tu perfil para recibir recomendaciones personalizadas.</p>
                    </div>
                )}
            </main>
        </div>
    );
}

export default WorldMapPage;
