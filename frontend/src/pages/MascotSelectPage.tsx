/**
 * Mascot Selection - Choose your companion
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import MascotCard from '../components/game/MascotCard';

export default function MascotSelectPage() {
    const navigate = useNavigate();
    const [selected, setSelected] = useState('leo');
    const [celebrating, setCelebrating] = useState(false);

    const handleSelect = () => {
        setCelebrating(true);
        setTimeout(() => {
            navigate('/world');
        }, 1000);
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-900 via-purple-900 to-gray-900 flex flex-col items-center justify-center p-4">
            {/* Header */}
            <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-white mb-2">¡Elige tu compañero!</h1>
                <p className="text-gray-400">Te acompañará en tu aventura de aprendizaje</p>
            </div>

            {/* Mascot Card */}
            <div className="mb-8">
                <MascotCard
                    name="Leo el Gatito"
                    level="A1"
                    vocab={0}
                    streak={0}
                    xp={0}
                    isAnimating={true}
                    onCelebrate={celebrating}
                />
            </div>

            {/* More mascots coming soon */}
            <div className="flex gap-4 mb-8 opacity-50">
                <div className="w-16 h-16 bg-gray-700 rounded-xl flex items-center justify-center text-2xl">
                    🐶
                </div>
                <div className="w-16 h-16 bg-gray-700 rounded-xl flex items-center justify-center text-2xl">
                    🦊
                </div>
                <div className="w-16 h-16 bg-gray-700 rounded-xl flex items-center justify-center text-2xl">
                    🐰
                </div>
                <p className="text-gray-500 text-xs self-center">Próximamente...</p>
            </div>

            {/* Select button */}
            <button
                onClick={handleSelect}
                className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold text-lg rounded-2xl shadow-lg shadow-purple-500/30 hover:shadow-xl hover:-translate-y-1 transition-all"
            >
                ¡Elegir a Leo! 🐱
            </button>
        </div>
    );
}
