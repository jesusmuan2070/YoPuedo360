/**
 * MascotBuddy - Floating companion in corner of screen
 * Greets user when they return to the app (tab visibility)
 */

import { useState, useEffect, useCallback } from 'react';

// Import greeting animation frames
import leoGreeting01 from '../../assets/mascots/leo/A1/greeting/leo_greeting_01.png';
import leoGreeting02 from '../../assets/mascots/leo/A1/greeting/leo_greeting_02.png';
import leoGreeting03 from '../../assets/mascots/leo/A1/greeting/leo_greeting_03.png';
//import leoGreeting04 from '../../assets/mascots/leo/A1/greeting/leo_greeting_04.png';

// Animation sequences
const IDLE_FRAMES = [leoGreeting01];
const GREETING_FRAMES = [leoGreeting01, leoGreeting02, leoGreeting03, leoGreeting02, leoGreeting01];

export default function MascotBuddy({
    message = '',
    welcomeMessage = '¡Hola! ¿Listo para aprender?',
    onClick = () => { },
    size = 'md',
}) {
    const [currentFrame, setCurrentFrame] = useState(0);
    const [isGreeting, setIsGreeting] = useState(false);
    const [showMessage, setShowMessage] = useState(false);
    const [displayMessage, setDisplayMessage] = useState(message);

    // Get current frames based on animation state
    const currentFrames = isGreeting ? GREETING_FRAMES : IDLE_FRAMES;

    // Play greeting animation
    const playGreeting = useCallback(() => {
        setIsGreeting(true);
        setCurrentFrame(0);
        setDisplayMessage(welcomeMessage);
        setShowMessage(true);
    }, [welcomeMessage]);

    // Animation loop
    useEffect(() => {
        if (!isGreeting) return;

        const interval = setInterval(() => {
            setCurrentFrame(prev => {
                const nextFrame = prev + 1;
                if (nextFrame >= GREETING_FRAMES.length) {
                    // Animation finished
                    setIsGreeting(false);
                    setTimeout(() => setShowMessage(false), 2000);
                    return 0;
                }
                return nextFrame;
            });
        }, 150); // Faster for smoother wave

        return () => clearInterval(interval);
    }, [isGreeting]);

    // Detect when user returns to tab (visibility change)
    useEffect(() => {
        const handleVisibilityChange = () => {
            if (document.visibilityState === 'visible') {
                // User returned to tab!
                playGreeting();
            }
        };

        document.addEventListener('visibilitychange', handleVisibilityChange);

        // Also greet on first mount
        playGreeting();

        return () => {
            document.removeEventListener('visibilitychange', handleVisibilityChange);
        };
    }, [playGreeting]);

    // Handle custom message prop
    useEffect(() => {
        if (message) {
            setDisplayMessage(message);
            setShowMessage(true);
            const timer = setTimeout(() => setShowMessage(false), 3000);
            return () => clearTimeout(timer);
        }
    }, [message]);

    const sizes = {
        sm: 'w-16 h-16',
        md: 'w-24 h-24',
        lg: 'w-32 h-32',
    };

    return (
        <div className="fixed bottom-4 right-4 z-50">
            {/* Speech bubble */}
            {showMessage && displayMessage && (
                <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 bg-white rounded-xl px-3 py-2 shadow-lg text-sm max-w-48 text-center animate-bounce">
                    {displayMessage}
                    <div className="absolute top-full left-1/2 -translate-x-1/2 border-8 border-transparent border-t-white" />
                </div>
            )}

            {/* Mascot */}
            <button
                onClick={() => {
                    onClick();
                    playGreeting();
                }}
                className={`${sizes[size]} hover:scale-110 transition-transform cursor-pointer`}
            >
                <img
                    src={currentFrames[currentFrame] || IDLE_FRAMES[0]}
                    alt="Leo"
                    className="w-full h-full object-contain drop-shadow-lg"
                />
            </button>
        </div>
    );
}
