import { useState, useEffect, useRef, ChangeEvent } from 'react';
import { usersAPI } from '../services/api';
import type { User } from '../types';

export default function ProfilePage() {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);

    useEffect(() => {
        loadUser();
    }, []);

    const loadUser = async () => {
        try {
            const response = await usersAPI.getMe();
            setUser(response.data);
            setPreviewUrl(response.data.avatar_url);
        } catch (error) {
            console.error('Failed to load profile:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            // Create local preview
            const objectUrl = URL.createObjectURL(file);
            setPreviewUrl(objectUrl);
            setIsMenuOpen(false);

            // TODO: Implement actual upload to backend
            // Since backend currently only accepts a URL string for avatar_url,
            // we need a file upload endpoint or S3 integration.
            // For now, we show the preview to satisfy the UI requirement.
            alert("File selected! (Backend upload integration pending)");
        }
    };

    const handleTakePhoto = () => {
        setIsMenuOpen(false);
        alert("Camera feature coming soon!");
    };

    // Close menu when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            const target = event.target as HTMLElement;
            if (!target.closest('.avatar-edit-menu') && !target.closest('.avatar-edit-btn')) {
                setIsMenuOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            </div>
        );
    }

    if (!user) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <p className="text-gray-500">Profile not found</p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 pt-20 pb-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto">
                <div className="bg-white shadow rounded-lg overflow-hidden">
                    {/* Header bg */}
                    <div className="h-32 bg-gradient-to-r from-indigo-500 to-purple-600"></div>

                    <div className="relative px-6 pb-6">
                        {/* Avatar Section */}
                        <div className="absolute -top-16 flex items-end">
                            <div className="relative">
                                <div className="h-32 w-32 rounded-full border-4 border-white bg-white overflow-hidden shadow-md">
                                    {previewUrl ? (
                                        <img src={previewUrl} alt={user.username} className="h-full w-full object-cover" />
                                    ) : user.avatar_url ? (
                                        <img src={user.avatar_url} alt={user.username} className="h-full w-full object-cover" />
                                    ) : (
                                        <div className="h-full w-full bg-gray-200 flex items-center justify-center text-4xl text-gray-400 font-bold">
                                            {user.username.charAt(0).toUpperCase()}
                                        </div>
                                    )}
                                </div>

                                {/* Edit Button & Menu */}
                                <div className="absolute bottom-2 -right-20">
                                    <button
                                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                                        className="avatar-edit-btn flex items-center gap-1 text-cyan-500 font-semibold hover:text-cyan-600 transition-colors bg-white px-2 py-1 rounded-full shadow-sm"
                                    >
                                        <span className="text-sm">✏️</span>
                                        <span>Editar</span>
                                    </button>

                                    {/* Dropdown Menu */}
                                    {isMenuOpen && (
                                        <div className="avatar-edit-menu absolute top-full left-4 mt-2 w-48 bg-white rounded-xl shadow-xl py-2 z-10 border border-gray-100 transform origin-top-left">
                                            {/* Speech bubble arrow */}
                                            <div className="absolute -top-2 left-6 w-4 h-4 bg-white transform rotate-45 border-t border-l border-gray-100"></div>

                                            <button
                                                onClick={() => fileInputRef.current?.click()}
                                                className="w-full text-left px-4 py-3 text-gray-700 hover:bg-gray-50 transition-colors text-sm"
                                            >
                                                Subir una foto
                                            </button>
                                            <button
                                                onClick={handleTakePhoto}
                                                className="w-full text-left px-4 py-3 text-gray-700 hover:bg-gray-50 transition-colors text-sm"
                                            >
                                                Tomar Foto
                                            </button>
                                        </div>
                                    )}

                                    <input
                                        type="file"
                                        ref={fileInputRef}
                                        className="hidden"
                                        accept="image/*"
                                        onChange={handleFileChange}
                                    />
                                </div>
                            </div>
                        </div>

                        {/* User Info */}
                        <div className="mt-16">
                            <h1 className="text-3xl font-bold text-gray-900">{user.username}</h1>
                            <p className="text-sm text-gray-500">{user.email}</p>
                        </div>

                        {/* Stats Grid */}
                        <div className="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-3">
                            <div className="bg-gray-50 overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6">
                                <dt className="text-sm font-medium text-gray-500 truncate">Current Level</dt>
                                <dd className="mt-1 text-3xl font-semibold text-gray-900">{user.learning_profile?.current_level || 1}</dd>
                            </div>
                            <div className="bg-gray-50 overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6">
                                <dt className="text-sm font-medium text-gray-500 truncate">Total XP</dt>
                                <dd className="mt-1 text-3xl font-semibold text-gray-900">{user.learning_profile?.total_xp || 0}</dd>
                            </div>
                            <div className="bg-gray-50 overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6">
                                <dt className="text-sm font-medium text-gray-500 truncate">Day Streak</dt>
                                <dd className="mt-1 text-3xl font-semibold text-gray-900">{user.learning_profile?.streak_days || 0} 🔥</dd>
                            </div>
                        </div>

                        {/* Language Info */}
                        <div className="mt-8 border-t border-gray-200 pt-6">
                            <h2 className="text-lg font-medium text-gray-900">Learning Details</h2>
                            <dl className="mt-4 grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
                                <div>
                                    <dt className="text-sm font-medium text-gray-500">Learning Goal</dt>
                                    <dd className="mt-1 text-sm text-gray-900 capitalize">{user.learning_profile?.learning_goal || 'General'}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm font-medium text-gray-500">Daily Goal</dt>
                                    <dd className="mt-1 text-sm text-gray-900">{user.learning_profile?.daily_goal_minutes || 15} minutes/day</dd>
                                </div>
                                <div>
                                    <dt className="text-sm font-medium text-gray-500">Native Language</dt>
                                    <dd className="mt-1 text-sm text-gray-900 uppercase">{user.learning_profile?.native_language || 'ES'}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm font-medium text-gray-500">Target Language</dt>
                                    <dd className="mt-1 text-sm text-gray-900 uppercase">{user.learning_profile?.target_language || 'EN'}</dd>
                                </div>
                            </dl>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
