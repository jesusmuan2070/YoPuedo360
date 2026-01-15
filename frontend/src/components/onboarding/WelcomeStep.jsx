/**
 * Welcome Step - Compact design
 */

import { Link } from 'react-router-dom';

export default function WelcomeStep({ onComplete }) {
    return (
        <div className="text-center">
            <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                <span className="text-4xl">🧠</span>
            </div>

            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
                ¡Bienvenido!
            </h1>
            <p className="text-gray-500 text-sm mb-6">
                Personalicemos tu experiencia de aprendizaje
            </p>

            <div className="grid grid-cols-2 gap-3 mb-6">
                <div className="bg-purple-50 rounded-xl p-3 text-center">
                    <span className="text-2xl">🎯</span>
                    <p className="text-xs text-gray-600 mt-1">Tu estilo</p>
                </div>
                <div className="bg-pink-50 rounded-xl p-3 text-center">
                    <span className="text-2xl">🏰</span>
                    <p className="text-xs text-gray-600 mt-1">Memory Palace</p>
                </div>
                <div className="bg-orange-50 rounded-xl p-3 text-center">
                    <span className="text-2xl">🤖</span>
                    <p className="text-xs text-gray-600 mt-1">IA adaptativa</p>
                </div>
                <div className="bg-green-50 rounded-xl p-3 text-center">
                    <span className="text-2xl">🔥</span>
                    <p className="text-xs text-gray-600 mt-1">Tu streak</p>
                </div>
            </div>

            <button
                onClick={() => onComplete({})}
                className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl shadow-lg shadow-purple-500/30 hover:shadow-xl hover:-translate-y-0.5 transition-all"
            >
                Comenzar 🚀
            </button>

            <p className="text-gray-400 text-xs mt-4">
                ¿Ya tienes cuenta? <Link to="/login" className="text-purple-600 font-medium">Inicia sesión</Link>
            </p>
        </div>
    );
}
