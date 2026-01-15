/**
 * ScenarioCard - Card component for displaying a scenario
 * Uses Tailwind CSS
 */

// Mapping of scenario slugs to images (in public folder)
const scenarioImages = {
    'movies': '/scenarios/cinema.png',
    'gaming': '/scenarios/gaming.png',
    'gym': '/scenarios/gym.png',
    'doctor': '/scenarios/doctor.png',
    'pharmacy': '/scenarios/pharmacy.png',
    'office': '/scenarios/office.jpg',
    'cooking': '/scenarios/cooking.jpg',
    'university': '/scenarios/university.jpg',
    // Add more as we generate them
};

function ScenarioCard({ scenario, rank, onClick }) {
    const { slug, name, icon, description, difficulty_min, difficulty_max, milestones_count } = scenario;

    // Check if we have an image for this scenario
    const hasImage = scenarioImages[slug];

    // Border accent for top 3
    const getBorderClass = () => {
        if (rank === 1) return 'border-yellow-400/50 bg-gradient-to-br from-yellow-500/10 to-transparent';
        if (rank === 2) return 'border-gray-400/50 bg-gradient-to-br from-gray-400/10 to-transparent';
        if (rank === 3) return 'border-amber-600/50 bg-gradient-to-br from-amber-600/10 to-transparent';
        return 'border-white/10 bg-white/5';
    };

    // Get first letter as fallback
    const getInitial = () => {
        return name?.charAt(0)?.toUpperCase() || '?';
    };

    return (
        <div
            className={`relative flex items-center gap-4 p-4 rounded-2xl border cursor-pointer transition-all duration-300 hover:bg-white/10 hover:-translate-y-1 hover:shadow-xl hover:shadow-black/20 ${getBorderClass()}`}
            onClick={onClick}
            role="button"
            tabIndex={0}
            onKeyPress={(e) => e.key === 'Enter' && onClick()}
        >
            {/* Rank Badge */}
            {rank <= 3 && (
                <div className={`absolute -top-2 -left-2 w-8 h-8 flex items-center justify-center rounded-full text-xs font-bold shadow-lg ${rank === 1 ? 'bg-gradient-to-br from-yellow-400 to-yellow-600 text-yellow-900' :
                    rank === 2 ? 'bg-gradient-to-br from-gray-300 to-gray-500 text-gray-800' :
                        'bg-gradient-to-br from-amber-500 to-amber-700 text-amber-900'
                    }`}>
                    #{rank}
                </div>
            )}

            {/* 
              TAMAÑO DE IMAGEN - Aquí controlas el tamaño:
              - min-w-[64px] w-[64px] h-[64px] = tamaño del CONTENEDOR
              - w-16 h-16 = tamaño de la IMAGEN (16 = 64px en Tailwind)
              
              Para cambiar: 
                Pequeño:  w-[50px] y w-12 h-12 (48px)
                Mediano:  w-[64px] y w-16 h-16 (64px)
                Grande:   w-[80px] y w-20 h-20 (80px) ← ACTUAL
                XGrande:  w-[96px] y w-24 h-24 (96px)
            */}
            <div className="min-w-[80px] w-[80px] h-[80px] flex items-center justify-center">
                {hasImage ? (
                    <img
                        src={scenarioImages[slug]}
                        alt={name}
                        className="w-20 h-20 object-cover rounded-xl"
                    />
                ) : icon && !icon.includes('?') ? (
                    <span className="text-5xl">{icon}</span>
                ) : (
                    <div className="w-20 h-20 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold text-2xl">
                        {getInitial()}
                    </div>
                )}
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0">
                <h3 className="text-white font-semibold truncate">
                    {name}
                </h3>
                <p className="text-white/50 text-sm line-clamp-2 mt-1">
                    {description}
                </p>

                {/* Metadata */}
                <div className="flex flex-wrap gap-2 mt-2">
                    <span className="text-xs px-2 py-1 bg-white/5 rounded text-cyan-400">
                        {difficulty_min || 'A1'}{difficulty_max && difficulty_max !== difficulty_min && ` - ${difficulty_max}`}
                    </span>
                    {milestones_count > 0 && (
                        <span className="text-xs px-2 py-1 bg-white/5 rounded text-emerald-400">
                            {milestones_count} lecciones
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
}

export default ScenarioCard;

