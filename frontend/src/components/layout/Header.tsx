/**
 * Header Component
 * Main navigation header with logo, nav links, and stats bar
 */

import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useStats } from '../../context/StatsContext';
import { useAuth } from '../../context/AuthContext';
import LanguageDropdown from './LanguageDropdown';

interface HeaderProps {
    /** Whether to show the stats (only when logged in) */
    showStats?: boolean;
}

export default function Header({ showStats = true }: HeaderProps) {
    const location = useLocation();
    const { stats } = useStats();
    const { user, logout } = useAuth();
    const [isProfileOpen, setIsProfileOpen] = useState(false);
    const [activeCourses, setActiveCourses] = useState<string[]>([]);



    const isActive = (path: string) => location.pathname === path;

    // Calculate daily progress percentage from context stats
    const dailyProgress = stats
        ? Math.min(100, Math.round((stats.today_minutes / stats.daily_goal_minutes) * 100))
        : 0;



    return (
        <header className="sticky top-0 z-50 bg-white shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">

                    {/* Left side: Logo + Nav */}
                    <div className="flex items-center gap-8">
                        {/* Logo */}
                        <Link to="/" className="flex items-center gap-2">
                            <span className="text-2xl font-bold bg-gradient-to-r from-[#667eea] to-[#764ba2] bg-clip-text text-transparent">
                                YP
                            </span>
                        </Link>

                        {/* Navigation Links */}
                        <nav className="hidden md:flex items-center gap-6">
                            <Link
                                to="/world"
                                className={`font-medium transition-colors ${isActive('/world')
                                    ? 'text-[#667eea]'
                                    : 'text-gray-600 hover:text-[#667eea]'
                                    }`}
                            >
                                Learn
                            </Link>
                            <Link
                                to="/chats"
                                className={`font-medium transition-colors ${isActive('/chats')
                                    ? 'text-[#667eea]'
                                    : 'text-gray-600 hover:text-[#667eea]'
                                    }`}
                            >
                                Chats
                            </Link>
                        </nav>
                    </div>

                    {/* Right side: Stats */}
                    {showStats && user && stats && (
                        <div className="flex items-center gap-4 md:gap-6">
                            {/* Language Dropdown */}
                            <LanguageDropdown
                                targetLanguage={user?.learning_profile?.target_language || 'en'}
                                nativeLanguage={user?.learning_profile?.native_language || 'es'}
                                activeCourses={activeCourses}
                                onAddCourse={(lang) => {
                                    // Add to local state (later: persist to backend)
                                    setActiveCourses(prev => [...prev, lang]);
                                    console.log('Added course:', lang);
                                }}
                                onSwitchCourse={(lang) => {
                                    // TODO: Call API to switch active course
                                    console.log('Switch to', lang);
                                }}
                            />

                            {/* Streak */}
                            <div
                                className="flex items-center gap-1 cursor-pointer hover:opacity-80 transition-opacity"
                                title="Daily streak"
                            >
                                <span className="text-xl" style={{
                                    filter: stats.streak_days > 0 ? 'drop-shadow(0 0 4px #ff9500)' : 'none'
                                }}>
                                    🔥
                                </span>
                                <span className="font-semibold text-gray-700">{stats.streak_days}</span>
                            </div>

                            {/* XP */}
                            <div
                                className="flex items-center gap-1 cursor-pointer hover:opacity-80 transition-opacity"
                                title="Total XP"
                            >
                                <span className="text-xl" style={{
                                    filter: 'drop-shadow(0 0 3px #ffd700)'
                                }}>
                                    ⚡
                                </span>
                                <span className="font-semibold text-gray-700">
                                    {stats.total_xp.toLocaleString()} XP
                                </span>
                            </div>

                            {/* Level */}
                            <div
                                className="hidden sm:flex items-center gap-1 cursor-pointer hover:opacity-80 transition-opacity"
                                title="Current level"
                            >
                                <span className="text-xl" style={{
                                    filter: 'drop-shadow(0 0 3px #9b59b6)'
                                }}>
                                    👑
                                </span>
                                <span className="font-semibold text-gray-700">
                                    Lvl {stats.current_level}
                                </span>
                            </div>

                            {/* Daily Progress Ring */}
                            <div
                                className="hidden sm:flex items-center cursor-pointer hover:opacity-80 transition-opacity"
                                title={`${stats.today_minutes}/${stats.daily_goal_minutes} minutes today`}
                            >
                                <div className="relative w-10 h-10">
                                    {/* Background circle */}
                                    <svg className="w-10 h-10 transform -rotate-90">
                                        <circle
                                            cx="20"
                                            cy="20"
                                            r="16"
                                            stroke="#e5e7eb"
                                            strokeWidth="3"
                                            fill="none"
                                        />
                                        {/* Progress circle */}
                                        <circle
                                            cx="20"
                                            cy="20"
                                            r="16"
                                            stroke="url(#progressGradient)"
                                            strokeWidth="3"
                                            fill="none"
                                            strokeLinecap="round"
                                            strokeDasharray={`${dailyProgress} 100`}
                                            className="transition-all duration-500"
                                        />
                                        <defs>
                                            <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                                <stop offset="0%" stopColor="#667eea" />
                                                <stop offset="100%" stopColor="#764ba2" />
                                            </linearGradient>
                                        </defs>
                                    </svg>
                                    {/* Text in center */}
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        <span className="text-[10px] font-bold text-gray-600">
                                            {stats.today_minutes}/{stats.daily_goal_minutes}
                                        </span>
                                    </div>
                                </div>
                            </div>

                            {/* Profile Dropdown */}
                            <div className="relative">
                                <button
                                    onClick={() => setIsProfileOpen(!isProfileOpen)}
                                    className="w-9 h-9 rounded-full bg-gradient-to-br from-[#667eea] to-[#764ba2] flex items-center justify-center text-white font-semibold text-sm hover:opacity-90 transition-opacity overflow-hidden ring-2 ring-offset-2 ring-transparent hover:ring-[#667eea] focus:outline-none"
                                >
                                    {user?.avatar_url ? (
                                        <img
                                            src={user.avatar_url}
                                            alt="Profile"
                                            className="w-full h-full object-cover"
                                        />
                                    ) : (
                                        user?.username?.charAt(0).toUpperCase() || 'U'
                                    )}
                                </button>

                                {/* Dropdown Menu */}
                                {isProfileOpen && (
                                    <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg py-2 z-50 ring-1 ring-black ring-opacity-5 transform origin-top-right transition-all duration-200">
                                        <Link
                                            to="/profile"
                                            className="px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-3 transition-colors"
                                            onClick={() => setIsProfileOpen(false)}
                                        >
                                            <span className="text-lg">👤</span>
                                            My profile
                                        </Link>
                                        <Link
                                            to="/settings"
                                            className="px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-3 transition-colors"
                                            onClick={() => setIsProfileOpen(false)}
                                        >
                                            <span className="text-lg">⚙️</span>
                                            Settings
                                        </Link>
                                        <button
                                            className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-3 transition-colors"
                                            onClick={() => setIsProfileOpen(false)}
                                        >
                                            <span className="text-lg">👥</span>
                                            Invite friends
                                        </button>

                                        <div className="border-t border-gray-100 my-1"></div>

                                        <button
                                            onClick={() => {
                                                setIsProfileOpen(false);
                                                logout();
                                            }}
                                            className="w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 flex items-center gap-3 transition-colors"
                                        >
                                            <span className="text-lg">🚪</span>
                                            Logout
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Auth links when not showing stats */}
                    {!showStats && (
                        <div className="flex items-center gap-4">
                            <Link
                                to="/login"
                                className="text-gray-600 hover:text-[#667eea] font-medium transition-colors"
                            >
                                Login
                            </Link>
                            <Link
                                to="/register"
                                className="btn-primary px-4 py-2 text-sm"
                            >
                                Get Started
                            </Link>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
}
