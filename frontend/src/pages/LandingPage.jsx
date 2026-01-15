/**
 * Landing Page - Main entry point (Duolingo-inspired)
 */

import { Link } from 'react-router-dom';

export default function LandingPage() {
    return (
        <div className="min-h-screen bg-white">
            {/* Header */}
            <header className="flex justify-between items-center px-6 py-4 max-w-7xl mx-auto">
                <div className="flex items-center gap-2">
                    <span className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                        YoPuedo360
                    </span>
                </div>
                <Link
                    to="/login"
                    className="text-purple-600 font-semibold hover:text-purple-700"
                >
                    Iniciar Sesión
                </Link>
            </header>

            {/* Hero Section */}
            <main className="max-w-7xl mx-auto px-6 py-12 md:py-20">
                <div className="flex flex-col md:flex-row items-center gap-12">
                    {/* Illustration */}
                    <div className="flex-1 flex justify-center">
                        <div className="relative w-96 h-96 md:w-96 md:h-96">
                            {/* Background circles */}
                            <div className="absolute inset-0 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full animate-pulse blur-xl"></div>

                            {/* Character/Icons arrangement */}
                            <div className="absolute inset-0 flex items-center justify-center">
                                <div className="relative">
                                    {/* Center brain */}
                                    <div className="text-8xl animate-bounce">🧠</div>

                                    {/* Floating elements */}
                                    <div className="absolute -top-8 -left-12 text-4xl animate-float">📚</div>
                                    <div className="absolute -top-4 -right-16 text-4xl animate-float-delay">🎯</div>
                                    <div className="absolute -bottom-4 -left-16 text-4xl animate-float">🏰</div>
                                    <div className="absolute -bottom-8 -right-12 text-4xl animate-float-delay">⭐</div>
                                    <div className="absolute top-12 -right-20 text-3xl animate-float">🔥</div>
                                    <div className="absolute top-12 -left-20 text-3xl animate-float-delay">💬</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Content */}
                    <div className="flex-1 text-center md:text-left">
                        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight mb-6">
                            ¡La forma divertida y
                            <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent"> personalizada </span>
                            de aprender idiomas!
                        </h1>

                        <p className="text-xl text-gray-600 mb-10">
                            Construye tu Palacio de Memoria, aprende a tu ritmo y descubre tu estilo único de aprendizaje.
                        </p>

                        <div className="space-y-4 max-w-sm mx-auto md:mx-0">
                            <Link
                                to="/onboarding"
                                className="block w-full py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white text-center font-bold text-lg rounded-2xl shadow-lg shadow-purple-500/30 hover:shadow-xl hover:shadow-purple-500/40 hover:-translate-y-1 transition-all"
                            >
                                EMPIEZA AHORA
                            </Link>

                            <Link
                                to="/login"
                                className="block w-full py-4 bg-white text-purple-600 text-center font-bold text-lg rounded-2xl border-2 border-gray-200 hover:border-purple-300 hover:bg-purple-50 transition-all"
                            >
                                YA TENGO UNA CUENTA
                            </Link>
                        </div>
                    </div>
                </div>
            </main>

            {/* Features Section */}
            <section className="bg-white/10 py-16">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="text-center p-6">
                            <div className="w-18 h-18 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <img src="/scenarios/your_style.png" alt="Personalizado para ti" className="w-full h-full object-cover rounded-xl" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-700 mb-2">Personalizado para ti</h3>
                            <p className="text-gray-500">Descubre si eres visual, auditivo o kinestésico y aprende a tu manera.</p>
                        </div>

                        <div className="text-center p-6">
                            <div className="w-18 h-18 bg-gradient-to-br from-orange-400 to-red-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <img src="/scenarios/memory_palace.png" alt="Tu Palacio de Memoria" className="w-full h-full object-cover rounded-xl" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-700 mb-2">Tu Palacio de Memoria</h3>
                            <p className="text-gray-500">Construye mundos y memoriza vocabulario usando técnicas de memory palace.</p>
                        </div>

                        <div className="text-center p-6">
                            <div className="w-18 h-18 bg-gradient-to-br from-green-400 to-emerald-500 rounded-xl flex items-center justify-center mx-auto mb-4">
                                <img src="/scenarios/adaptive_ai.png" alt="IA que te entiende" className="w-full h-full object-cover rounded-xl" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-700 mb-2">IA que te entiende</h3>
                            <p className="text-gray-500">Retroalimentación inteligente que se adapta a tu progreso.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Problem Section - COMMENTED OUT FOR REVIEW */}
            {/*
            <section className="py-16 bg-white">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="flex flex-col md:flex-row items-center gap-12">

                        <div className="flex-1">
                            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight mb-6">
                                ¿Estudias pero
                                <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                                    {" "}te quedas en blanco{" "}
                                </span>
                                cuando lo necesitas?
                            </h2>

                            <p className="text-xl text-gray-600">
                                Sabes vocabulario. Conoces reglas.
                                <br />
                                Pero en una reunión, un viaje o una llamada real…
                                <br />
                                <strong className="text-gray-800">no sabes qué decir.</strong>
                            </p>
                        </div>

                        <div className="flex-1">
                            <div className="rounded-2xl shadow-xl overflow-hidden">
                                <img
                                    src="/scenarios/isolated_words_problem.png"
                                    alt="Persona aislada en una conversación"
                                    className="w-full h-full object-cover"
                                />
                            </div>
                        </div>

                    </div>
                </div>
            </section>
            */}

            {/* Solution Section - COMMENTED OUT FOR REVIEW */}
            {/*
            <section className="py-16 bg-white">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="flex flex-col md:flex-row items-center gap-12">

                        <div className="flex-1">
                            <div className="flex flex-col gap-3">
                                <span className="px-4 py-3 text-green-700 rounded-xl text-sm font-medium">
                                    Practicas frases completas, no palabras sueltas
                                </span>
                                <span className="px-4 py-3 text-green-700 rounded-xl text-sm font-medium">
                                    Aprendes dentro de escenarios reales
                                </span>
                                <span className="px-4 py-3 text-green-700 rounded-xl text-sm font-medium">
                                    Contenido adaptado a tu trabajo y objetivos
                                </span>
                                <span className="px-4 py-3 text-green-700 rounded-xl text-sm font-medium">
                                    Sabes qué decir antes de necesitarlo
                                </span>
                            </div>

                            <Link
                                to="/onboarding"
                                className="block w-full py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white text-center font-bold text-lg rounded-2xl shadow-lg shadow-purple-500/30 hover:shadow-xl hover:shadow-purple-500/40 hover:-translate-y-1 transition-all mt-6"
                            >
                                EMPIEZA AHORA
                            </Link>
                        </div>

                        <div className="flex-1">
                            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight mb-6">
                                En YoPuedo360
                                <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                                    {" "}aprendes idiomas{" "}
                                </span>
                                y lo usas en la vida real
                            </h2>

                            <p className="text-xl text-gray-600">
                                Cada lección te prepara para hablar con confianza,
                                <br />
                                <strong className="text-gray-800">
                                    y no sólo para memorizar.
                                </strong>
                            </p>
                        </div>

                    </div>
                </div>
            </section>
            */}

            {/* Footer */}
            <footer className="py-8 text-center text-gray-500 text-sm">
                <p>© 2026 YoPuedo360. Todos los derechos reservados.</p>
            </footer>
        </div>
    );
}
