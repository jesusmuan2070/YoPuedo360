/**
 * Language Dropdown Component
 * Duolingo-style dropdown for selecting/viewing language courses
 */

import { useState, useRef, useEffect } from 'react';
import { LANGUAGE_FLAGS, LANGUAGE_NAMES } from '../../types';

interface LanguageDropdownProps {
    /** Current target language code (e.g., 'en', 'es') */
    targetLanguage: string;
    /** Current native language code */
    nativeLanguage: string;
    /** User's active courses (language codes they're learning) */
    activeCourses?: string[];
    /** Callback when user confirms adding a new course */
    onAddCourse?: (languageCode: string) => void;
    /** Callback when user selects a different active course */
    onSwitchCourse?: (languageCode: string) => void;
}

// Available language courses
const AVAILABLE_COURSES = ['en', 'es', 'fr', 'de', 'it', 'pt', 'zh', 'ja', 'ko'];

export default function LanguageDropdown({
    targetLanguage,
    nativeLanguage,
    activeCourses = [],
    onAddCourse,
    onSwitchCourse,
}: LanguageDropdownProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [selectedNewLanguage, setSelectedNewLanguage] = useState<string | null>(null);
    const dropdownRef = useRef<HTMLDivElement>(null);

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false);
                setSelectedNewLanguage(null); // Reset selection when closing
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    // Close on Escape key
    useEffect(() => {
        const handleEscape = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                setIsOpen(false);
                setSelectedNewLanguage(null);
            }
        };

        document.addEventListener('keydown', handleEscape);
        return () => document.removeEventListener('keydown', handleEscape);
    }, []);

    const currentFlag = LANGUAGE_FLAGS[targetLanguage] || '🌍';
    const currentName = LANGUAGE_NAMES[targetLanguage] || targetLanguage;
    const nativeFlag = LANGUAGE_FLAGS[nativeLanguage] || '🌍';
    const nativeName = LANGUAGE_NAMES[nativeLanguage] || nativeLanguage;

    // Combine active courses: the current target + any additional courses the user has
    const allActiveCourses = [targetLanguage, ...activeCourses.filter(c => c !== targetLanguage)];

    // Languages available to add (not native, not already active)
    const availableToAdd = AVAILABLE_COURSES.filter(
        lang => lang !== nativeLanguage && !allActiveCourses.includes(lang)
    );

    const handleAddCourse = () => {
        if (selectedNewLanguage) {
            onAddCourse?.(selectedNewLanguage);
            setSelectedNewLanguage(null);
            setIsOpen(false);
        }
    };

    return (
        <div className="relative" ref={dropdownRef}>
            {/* Trigger Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-1 p-1 rounded-lg hover:bg-gray-100 transition-colors"
                title={`Learning ${currentName}`}
                aria-expanded={isOpen}
                aria-haspopup="true"
            >
                <span className="text-2xl">{currentFlag}</span>
                <svg
                    className={`w-4 h-4 text-gray-500 transition-transform ${isOpen ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
            </button>

            {/* Dropdown Panel */}
            {isOpen && (
                <div className="absolute top-full left-0 mt-2 w-80 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden z-50 animate-fadeIn">
                    {/* Header */}
                    <div className="px-4 py-3 bg-gray-50 border-b border-gray-100">
                        <div className="flex items-center justify-between">
                            <h3 className="font-semibold text-gray-800">Mis cursos</h3>
                            <span className="text-xs text-gray-500 flex items-center gap-1">
                                Hablo {nativeFlag} {nativeName}
                            </span>
                        </div>
                    </div>

                    {/* Active Courses */}
                    <div className="p-3 space-y-2">
                        {allActiveCourses.map((lang) => {
                            const isCurrentCourse = lang === targetLanguage;
                            const flag = LANGUAGE_FLAGS[lang] || '🌍';
                            const name = LANGUAGE_NAMES[lang] || lang;

                            return (
                                <button
                                    key={lang}
                                    onClick={() => {
                                        if (!isCurrentCourse) {
                                            onSwitchCourse?.(lang);
                                            setIsOpen(false);
                                        }
                                    }}
                                    className={`w-full flex items-center gap-3 p-3 rounded-lg border transition-all ${isCurrentCourse
                                            ? 'bg-gradient-to-r from-[#667eea]/10 to-[#764ba2]/10 border-[#667eea]/20'
                                            : 'bg-white border-gray-200 hover:border-[#667eea]/40 hover:bg-gray-50'
                                        }`}
                                >
                                    <span className="text-3xl">{flag}</span>
                                    <div className="flex-1 text-left">
                                        <p className="font-semibold text-gray-800">{name}</p>
                                        <p className="text-xs text-gray-500">
                                            {isCurrentCourse ? 'Curso activo' : 'Cambiar a este curso'}
                                        </p>
                                    </div>
                                    {isCurrentCourse && (
                                        <div className="w-6 h-6 bg-[#667eea] rounded-full flex items-center justify-center">
                                            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                            </svg>
                                        </div>
                                    )}
                                </button>
                            );
                        })}
                    </div>

                    {/* Available Languages Grid */}
                    {availableToAdd.length > 0 && (
                        <div className="px-3 pb-3">
                            <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2 px-1">
                                Otros idiomas
                            </p>
                            <div className="grid grid-cols-3 gap-2">
                                {availableToAdd.map((lang) => {
                                    const isSelected = selectedNewLanguage === lang;
                                    return (
                                        <button
                                            key={lang}
                                            onClick={() => setSelectedNewLanguage(isSelected ? null : lang)}
                                            className={`flex flex-col items-center gap-1 p-3 rounded-lg transition-all group ${isSelected
                                                    ? 'bg-[#667eea]/10 ring-2 ring-[#667eea]'
                                                    : 'hover:bg-gray-100'
                                                }`}
                                        >
                                            <span className={`text-2xl transition-transform ${isSelected ? 'scale-110' : 'group-hover:scale-110'}`}>
                                                {LANGUAGE_FLAGS[lang] || '🌍'}
                                            </span>
                                            <span className={`text-xs font-medium ${isSelected ? 'text-[#667eea]' : 'text-gray-600'}`}>
                                                {LANGUAGE_NAMES[lang] || lang}
                                            </span>
                                            {isSelected && (
                                                <div className="absolute -top-1 -right-1 w-4 h-4 bg-[#667eea] rounded-full flex items-center justify-center">
                                                    <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                                    </svg>
                                                </div>
                                            )}
                                        </button>
                                    );
                                })}
                            </div>
                        </div>
                    )}

                    {/* Add Course Button */}
                    <div className="p-3 border-t border-gray-100">
                        <button
                            onClick={handleAddCourse}
                            disabled={!selectedNewLanguage}
                            className={`w-full flex items-center justify-center gap-2 py-2.5 px-4 font-medium rounded-lg transition-all ${selectedNewLanguage
                                    ? 'bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white hover:opacity-90'
                                    : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                }`}
                        >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                            </svg>
                            {selectedNewLanguage
                                ? `Agregar ${LANGUAGE_NAMES[selectedNewLanguage]}`
                                : 'Agregar curso'
                            }
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
