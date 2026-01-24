/**
 * TypeScript type definitions for YoPuedo360 API responses
 */

// User & Profile Types
export interface LearningProfile {
    native_language: string;
    target_language: string;
    learning_goal: string;
    daily_goal_minutes: number;
    current_level: number;
    total_xp: number;
    streak_days: number;
    cefr_level: string;
    profession: string;
    interests: Record<string, number>;
    hobbies: string[];
}

export interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    avatar_url: string | null;
    learning_profile: LearningProfile;
}

// Dashboard Types
export interface DashboardData {
    streak: number;
    longest_streak: number;
    current_level: number;
    total_xp: number;
    today_xp: number;
    today_minutes: number;
    daily_goal_minutes: number;
    daily_goal_met: boolean;
    last_7_days_xp: number[];
}

// Record Session Types
export interface RecordSessionRequest {
    minutes: number;
    xp_earned?: number;
    activity_type?: 'exercise' | 'lesson' | 'vocabulary' | 'grammar' | 'conversation';
}

export interface RecordSessionResponse {
    date: string;
    minutes_studied: number;
    daily_goal: number;
    daily_goal_met: boolean;
    just_completed_goal: boolean;
    bonus_xp_awarded: number;
    progress_percent: number;
    streak_days: number;
    total_xp: number;
    current_level: number;
}

// Activity History Types
export interface ActivityDay {
    date: string;
    minutes: number;
    xp: number;
    goal_met: boolean;
    exercises: number;
    lessons: number;
}

export interface ActivityHistoryResponse {
    results: ActivityDay[];
    total_days: number;
    days_active: number;
    total_minutes: number;
    total_xp: number;
}

// Streak Types
export interface StreakDetailResponse {
    current_streak: number;
    longest_streak: number;
    streak_start_date: string | null;
    weekly_activity: boolean[];
    is_at_risk: boolean;
}

// XP History Types
export interface XPHistoryResponse {
    current_level: number;
    total_xp: number;
    xp_to_next_level: number;
    xp_in_current_level: number;
    level_progress_percent: number;
    daily_xp: { date: string; xp: number }[];
}

// Settings Types
export interface UserSettings {
    daily_goal_minutes: number;
    learning_goal: string;
    preferred_ai_provider: string;
    native_language: string;
    target_language: string;
    notifications_enabled: boolean;
    reminder_time: string;
}

// Language flags mapping
export const LANGUAGE_FLAGS: Record<string, string> = {
    en: '🇺🇸',
    es: '🇪🇸',
    fr: '🇫🇷',
    de: '🇩🇪',
    it: '🇮🇹',
    pt: '🇧🇷',
    zh: '🇨🇳',
    ja: '🇯🇵',
    ko: '🇰🇷',
};

export const LANGUAGE_NAMES: Record<string, string> = {
    en: 'English',
    es: 'Español',
    fr: 'Français',
    de: 'Deutsch',
    it: 'Italiano',
    pt: 'Português',
    zh: '中文',
    ja: '日本語',
    ko: '한국어',
};
