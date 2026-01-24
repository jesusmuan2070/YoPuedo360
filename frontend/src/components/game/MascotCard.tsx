/**
 * MascotCard - Animated game-style character card
 */

import { useState, useEffect } from 'react';

// Import mascot frames
import leoBase from '../../assets/mascots/leo_base.jpg';
import leoFrame1 from '../../assets/mascots/leo_frame1.png';
import leoFrame2 from '../../assets/mascots/leo_frame2.png';
import leoFrame3 from '../../assets/mascots/leo_frame3.png';

const FRAMES = [leoFrame1, leoFrame2, leoFrame3, leoFrame2, leoFrame1];

const LEVEL_COLORS = {
    A1: 'from-green-400 to-emerald-500',
    A2: 'from-blue-400 to-cyan-500',
    B1: 'from-purple-400 to-violet-500',
    B2: 'from-orange-400 to-amber-500',
    C1: 'from-pink-400 to-rose-500',
    C2: 'from-yellow-400 to-orange-500',
};

export default function MascotCard({
    name = 'Leo el Gatito',
    level = 'A1',
    vocab = 0,
    streak = 0,
    xp = 0,
    isAnimating = true,
    onCelebrate = false,
}) {
    const [currentFrame, setCurrentFrame] = useState(0);
    const [celebrating, setCelebrating] = useState(false);

    // Greeting animation loop
    useEffect(() => {
        if (!isAnimating) return;

        const interval = setInterval(() => {
            setCurrentFrame(prev => (prev + 1) % FRAMES.length);
        }, 800); // Más lento: 800ms por frame

        return () => clearInterval(interval);
    }, [isAnimating]);

    // Celebration effect
    useEffect(() => {
        if (onCelebrate) {
            setCelebrating(true);
            setTimeout(() => setCelebrating(false), 600);
        }
    }, [onCelebrate]);

    return (
        <div className={`relative ${celebrating ? 'animate-bounce' : ''}`}>
            {/* Card container */}
            <div className="w-64 bg-gradient-to-b from-gray-900 to-gray-800 rounded-2xl p-1 shadow-2xl">

                {/* Level badge */}
                <div className="flex justify-between items-center px-3 py-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold text-white bg-gradient-to-r ${LEVEL_COLORS[level]}`}>
                        {level}
                    </span>
                    <span className="text-gray-400 text-xs">Básico</span>
                </div>

                {/* Mascot image - animated */}
                <div className="relative mx-2 rounded-xl overflow-hidden bg-gradient-to-b from-amber-100 to-green-200">
                    <img
                        src={FRAMES[currentFrame]}
                        alt={name}
                        className="w-full h-48 object-cover transition-all duration-100"
                        style={{ imageRendering: 'pixelated' }}
                    />

                    {/* Sparkles on celebrate */}
                    {celebrating && (
                        <div className="absolute inset-0 flex items-center justify-center">
                            <span className="text-4xl animate-ping">✨</span>
                        </div>
                    )}
                </div>

                {/* Name */}
                <div className="text-center py-2">
                    <h3 className="text-white font-bold text-lg">{name.toUpperCase()}</h3>
                </div>

                {/* Stats */}
                <div className="px-3 pb-3 space-y-2">
                    <div className="flex items-center justify-between text-sm">
                        <span className="flex items-center gap-2 text-gray-400">
                            <span className="text-lg">📚</span> Vocab
                        </span>
                        <span className="text-white font-bold">{vocab}</span>
                    </div>

                    <div className="flex items-center justify-between text-sm">
                        <span className="flex items-center gap-2 text-gray-400">
                            <span className="text-lg">🔥</span> Streak
                        </span>
                        <span className="text-orange-400 font-bold">{streak}</span>
                    </div>

                    <div className="flex items-center justify-between text-sm">
                        <span className="flex items-center gap-2 text-gray-400">
                            <span className="text-lg">⭐</span> XP
                        </span>
                        <span className="text-yellow-400 font-bold">{xp.toLocaleString()}</span>
                    </div>
                </div>

                {/* Total bar */}
                <div className="mx-3 mb-3 pt-2 border-t border-gray-700">
                    <div className="flex justify-between text-xs text-gray-500">
                        <span>TOTAL</span>
                        <span className="text-white font-bold">{vocab + streak + Math.floor(xp / 100)}</span>
                    </div>
                </div>
            </div>

            {/* Glow effect */}
            <div className={`absolute -inset-1 bg-gradient-to-r ${LEVEL_COLORS[level]} rounded-2xl blur opacity-20 -z-10`} />
        </div>
    );
}
