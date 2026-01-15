/**
 * ScenarioPage - Shows milestones within a scenario
 * Uses Tailwind CSS
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { progressAPI } from '../services/api';

function ScenarioPage() {
    const { slug } = useParams();
    const navigate = useNavigate();
    const [scenario, setScenario] = useState(null);
    const [milestones, setMilestones] = useState([]);
    const [progress, setProgress] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadScenarioData();
    }, [slug]);

    const loadScenarioData = async () => {
        try {
            setLoading(true);
            const response = await progressAPI.getScenarioProgress(slug);
            setScenario(response.data.scenario);
            setMilestones(response.data.milestones);
            setProgress(response.data.progress);
        } catch (err) {
            console.error('Error loading scenario:', err);
            setError('No se pudo cargar el escenario');
        } finally {
            setLoading(false);
        }
    };

    const handleMilestoneClick = async (milestone) => {
        if (milestone.status === 'completed') {
            return; // Already completed
        }

        try {
            if (milestone.status === 'not_started') {
                await progressAPI.startMilestone(milestone.id);
            }
            navigate(`/lesson/${milestone.id}`);
        } catch (err) {
            console.error('Error starting milestone:', err);
        }
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'completed': return '✅';
            case 'in_progress': return '🔄';
            default: return '⭐';
        }
    };

    const getStatusClass = (status) => {
        switch (status) {
            case 'completed': return 'border-emerald-500/40 bg-emerald-500/10';
            case 'in_progress': return 'border-cyan-500/40 bg-cyan-500/10';
            default: return 'border-white/10 bg-white/5';
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col items-center justify-center text-white">
                <div className="w-12 h-12 border-4 border-white/20 border-t-cyan-400 rounded-full animate-spin mb-4"></div>
                <p className="text-lg opacity-80">Cargando escenario...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col items-center justify-center text-white">
                <p className="text-lg mb-4">{error}</p>
                <button
                    onClick={() => navigate('/world')}
                    className="btn-primary px-8"
                >
                    Volver al mapa
                </button>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
            {/* Header */}
            <header className="flex items-center gap-4 p-6 bg-black/30 backdrop-blur-lg border-b border-white/10">
                <button
                    onClick={() => navigate('/world')}
                    className="px-4 py-2 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg text-sm transition-all"
                >
                    ← Volver
                </button>
                <div className="flex items-center gap-4">
                    <span className="text-4xl">{scenario?.icon || '📚'}</span>
                    <div>
                        <h1 className="text-xl font-bold">{scenario?.name}</h1>
                        <p className="text-sm text-white/50">{scenario?.slug}</p>
                    </div>
                </div>
            </header>

            {/* Progress Bar */}
            {progress && (
                <div className="px-6 py-4 bg-black/20">
                    <div className="flex justify-between text-sm text-white/70 mb-2">
                        <span>{progress.completed} de {progress.total} completados</span>
                        <span className="text-emerald-400 font-bold">{progress.percent}%</span>
                    </div>
                    <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-gradient-to-r from-cyan-400 to-emerald-400 rounded-full transition-all duration-500"
                            style={{ width: `${progress.percent}%` }}
                        ></div>
                    </div>
                </div>
            )}

            {/* Milestones List */}
            <main className="p-6 max-w-3xl mx-auto">
                <h2 className="text-lg font-semibold mb-4">📚 Lecciones</h2>
                <div className="flex flex-col gap-3">
                    {milestones.map((milestone, index) => (
                        <div
                            key={milestone.id}
                            className={`flex items-center gap-4 p-4 rounded-xl border cursor-pointer transition-all hover:translate-x-1 ${getStatusClass(milestone.status)}`}
                            onClick={() => handleMilestoneClick(milestone)}
                        >
                            <div className="w-9 h-9 flex items-center justify-center bg-white/10 rounded-full font-bold text-sm">
                                {index + 1}
                            </div>
                            <div className="flex-1">
                                <h3 className="font-medium">{milestone.name}</h3>
                                <div className="flex gap-3 mt-1 text-xs text-white/50">
                                    <span className="px-2 py-0.5 bg-cyan-500/20 text-cyan-400 rounded">
                                        {milestone.level}
                                    </span>
                                    <span>⏱️ {milestone.estimated_time} min</span>
                                    {milestone.best_score > 0 && (
                                        <span className="text-emerald-400">🏆 {milestone.best_score}%</span>
                                    )}
                                </div>
                            </div>
                            <div className="text-2xl">
                                {getStatusIcon(milestone.status)}
                            </div>
                        </div>
                    ))}
                </div>
            </main>
        </div>
    );
}

export default ScenarioPage;
