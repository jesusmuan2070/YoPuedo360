/**
 * StatsContext - Global state for user stats (XP, streak, etc.)
 * 
 * This context allows any component to update stats and have them
 * reflected across the app without refreshing.
 */

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { usersAPI } from '../services/api';
import { useAuth } from './AuthContext';

interface Stats {
    streak_days: number;
    total_xp: number;
    current_level: number;
    today_minutes: number;
    daily_goal_minutes: number;
    daily_goal_met: boolean;
}

interface StatsContextType {
    stats: Stats | null;
    loading: boolean;
    /** Refresh stats from API */
    refreshStats: () => Promise<void>;
    /** Update stats from a response (optimistic update) */
    updateStats: (updates: Partial<Stats>) => void;
}

const defaultStats: Stats = {
    streak_days: 0,
    total_xp: 0,
    current_level: 1,
    today_minutes: 0,
    daily_goal_minutes: 15,
    daily_goal_met: false,
};

const StatsContext = createContext<StatsContextType | null>(null);

export function StatsProvider({ children }: { children: ReactNode }) {
    const { isAuthenticated } = useAuth();
    const [stats, setStats] = useState<Stats | null>(null);
    const [loading, setLoading] = useState(true);

    // Load stats when authenticated
    useEffect(() => {
        if (isAuthenticated) {
            refreshStats();
        } else {
            setStats(null);
            setLoading(false);
        }
    }, [isAuthenticated]);

    const refreshStats = async () => {
        try {
            const response = await usersAPI.getDashboard();
            const data = response.data;

            setStats({
                streak_days: data.streak,  // Backend returns 'streak', we normalize to 'streak_days'
                total_xp: data.total_xp,
                current_level: data.current_level,
                today_minutes: data.today_minutes,
                daily_goal_minutes: data.daily_goal_minutes,
                daily_goal_met: data.daily_goal_met,
            });
        } catch (error) {
            console.error('Failed to load stats:', error);
            setStats(defaultStats);
        } finally {
            setLoading(false);
        }
    };

    const updateStats = (updates: Partial<Stats>) => {
        setStats(prev => prev ? { ...prev, ...updates } : { ...defaultStats, ...updates });
    };

    return (
        <StatsContext.Provider value={{ stats, loading, refreshStats, updateStats }}>
            {children}
        </StatsContext.Provider>
    );
}

export function useStats() {
    const context = useContext(StatsContext);
    if (!context) {
        throw new Error('useStats must be used within a StatsProvider');
    }
    return context;
}
