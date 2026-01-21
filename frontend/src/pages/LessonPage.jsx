/**
 * LessonPage - Intent-based learning page
 * Consumes content from the orchestrator API
 * Uses Tailwind CSS
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { orchestratorAPI } from '../services/api';

function LessonPage() {
    const { milestoneId } = useParams();
    const navigate = useNavigate();

    const [content, setContent] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentPhraseIndex, setCurrentPhraseIndex] = useState(0);

    useEffect(() => {
        loadContent();
    }, [milestoneId]);

    const loadContent = async () => {
        try {
            setLoading(true);
            const response = await orchestratorAPI.getMilestoneContent(milestoneId);
            console.log('🔍 Backend response:', response.data);
            setContent(response.data);
        } catch (err) {
            console.error('Error loading content:', err);
            setError('No se pudo cargar el contenido');
        } finally {
            setLoading(false);
        }
    };

    const handleNext = () => {
        if (content.target_phrases && currentPhraseIndex < content.target_phrases.length - 1) {
            setCurrentPhraseIndex(currentPhraseIndex + 1);
        }
    };

    const handlePrevious = () => {
        if (currentPhraseIndex > 0) {
            setCurrentPhraseIndex(currentPhraseIndex - 1);
        }
    };

    const handleComplete = async () => {
        try {
            if (content.current_intent.id) {
                await orchestratorAPI.completeIntent(content.current_intent.id, {
                    milestone_id: milestoneId,
                    score: 100
                });
            }
            navigate(-1); // Go back to scenario page
        } catch (err) {
            console.error('Error completing intent:', err);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col items-center justify-center text-white">
                <div className="w-12 h-12 border-4 border-white/20 border-t-cyan-400 rounded-full animate-spin mb-4"></div>
                <p className="text-lg opacity-80">Cargando lección...</p>
            </div>
        );
    }

    if (error || !content) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col items-center justify-center text-white px-6">
                <div className="max-w-md text-center">
                    <p className="text-6xl mb-4">🎯</p>
                    <h2 className="text-2xl font-bold mb-4">Contenido no disponible</h2>
                    <p className="text-lg mb-2 text-white/70">{error || 'No hay contenido disponible'}</p>
                    {content?.message && (
                        <p className="text-sm text-cyan-400 mb-6 bg-cyan-500/10 border border-cyan-500/30 rounded-lg p-4">
                            {content.message}
                        </p>
                    )}
                    <button
                        onClick={() => navigate(-1)}
                        className="px-8 py-3 bg-cyan-500 hover:bg-cyan-600 rounded-lg font-medium transition-all"
                    >
                        ← Volver al scenario
                    </button>
                </div>
            </div>
        );
    }

    // Check if orchestrator returned an error
    if (content.error) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col items-center justify-center text-white px-6">
                <div className="max-w-md text-center">
                    <p className="text-6xl mb-4">⚠️</p>
                    <h2 className="text-2xl font-bold mb-4">Intents no configurados</h2>
                    <p className="text-white/70 mb-6">
                        Este milestone aún no tiene intents disponibles. Estamos trabajando en agregar más contenido.
                    </p>
                    <div className="text-sm text-cyan-400 mb-6 bg-cyan-500/10 border border-cyan-500/30 rounded-lg p-4 text-left">
                        <p className="font-medium mb-2">Detalles técnicos:</p>
                        <p className="text-xs">{content.message}</p>
                    </div>
                    <button
                        onClick={() => navigate(-1)}
                        className="px-8 py-3 bg-cyan-500 hover:bg-cyan-600 rounded-lg font-medium transition-all"
                    >
                        ← Volver al scenario
                    </button>
                </div>
            </div>
        );
    }

    const currentPhrase = content.target_phrases?.[currentPhraseIndex];

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
            {/* Header */}
            <header className="flex items-center justify-between p-6 bg-black/30 backdrop-blur-lg border-b border-white/10">
                <button
                    onClick={() => navigate(-1)}
                    className="px-4 py-2 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg text-sm transition-all"
                >
                    ← Volver
                </button>

                <div className="text-center">
                    <h1 className="text-xl font-bold">{content.milestone?.name}</h1>
                    <p className="text-sm text-white/50">{content.milestone?.level}</p>
                </div>

                <div className="w-20"></div> {/* Spacer */}
            </header>

            {/* Progress Bar */}
            {content.progress && (
                <div className="px-6 py-4 bg-black/20">
                    <div className="flex justify-between text-sm text-white/70 mb-2">
                        <span>{content.progress.completed} de {content.progress.total} intents</span>
                        <span className="text-emerald-400 font-bold">{content.progress.percentage}%</span>
                    </div>
                    <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-gradient-to-r from-cyan-400 to-emerald-400 rounded-full transition-all duration-500"
                            style={{ width: `${content.progress.percentage}%` }}
                        ></div>
                    </div>
                </div>
            )}

            {/* Main Content */}
            <main className="p-6 max-w-4xl mx-auto space-y-6">
                {/* Current Intent */}
                <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <span className="text-3xl">🎯</span>
                        <div>
                            <h2 className="text-lg font-semibold">{content.current_intent?.name}</h2>
                            <p className="text-sm text-white/50">Objetivo comunicativo</p>
                        </div>
                    </div>
                </div>

                {/* Target Phrases */}
                {content.target_phrases && content.target_phrases.length > 0 && (
                    <div className="bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-2xl p-8">
                        <h3 className="text-sm font-medium text-cyan-300 mb-4">
                            Frase {currentPhraseIndex + 1} de {content.target_phrases.length}
                        </h3>

                        <div className="text-center mb-8">
                            <p className="text-3xl font-bold mb-2">{currentPhrase}</p>
                            <p className="text-white/50 text-sm">Practica esta frase</p>
                        </div>

                        {/* Navigation */}
                        <div className="flex justify-between items-center">
                            <button
                                onClick={handlePrevious}
                                disabled={currentPhraseIndex === 0}
                                className="px-6 py-2 bg-white/10 hover:bg-white/20 disabled:opacity-30 disabled:cursor-not-allowed rounded-lg transition-all"
                            >
                                ← Anterior
                            </button>

                            <span className="text-sm text-white/50">
                                {currentPhraseIndex + 1} / {content.target_phrases.length}
                            </span>

                            <button
                                onClick={handleNext}
                                disabled={currentPhraseIndex === content.target_phrases.length - 1}
                                className="px-6 py-2 bg-white/10 hover:bg-white/20 disabled:opacity-30 disabled:cursor-not-allowed rounded-lg transition-all"
                            >
                                Siguiente →
                            </button>
                        </div>
                    </div>
                )}

                {/* Supporting Grammar */}
                {content.supporting_grammar && content.supporting_grammar.length > 0 && (
                    <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                        <h3 className="text-lg font-semibold mb-4">📚 Gramática de Soporte</h3>
                        <div className="space-y-4">
                            {content.supporting_grammar.map((grammar, index) => (
                                <div key={index} className="bg-white/5 rounded-lg p-4">
                                    <h4 className="font-medium text-cyan-400 mb-2">{grammar.name}</h4>
                                    <p className="text-sm text-white/70 mb-2">{grammar.form}</p>
                                    {grammar.examples && grammar.examples.length > 0 && (
                                        <div className="text-sm text-white/50 space-y-1">
                                            {grammar.examples.slice(0, 2).map((example, i) => (
                                                <p key={i}>• {typeof example === 'object' ? example.en : example}</p>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Complete Button */}
                <div className="flex justify-center pt-4">
                    <button
                        onClick={handleComplete}
                        className="px-12 py-4 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
                    >
                        ✅ Completar Lección
                    </button>
                </div>
            </main>
        </div>
    );
}

export default LessonPage;
