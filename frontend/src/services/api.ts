/**
 * API Service for YoPuedo360
 * Handles all HTTP requests to the backend
 */

import axios, { AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import type {
    User,
    DashboardData,
    RecordSessionRequest,
    RecordSessionResponse,
    ActivityHistoryResponse,
    StreakDetailResponse,
    XPHistoryResponse,
    UserSettings,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with defaults
const api: AxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Debug: Log 401 errors
        if (error.response?.status === 401) {
            console.log('🔴 Got 401 error:', {
                url: originalRequest?.url,
                hasRetried: originalRequest?._retry,
                hasRefreshToken: !!localStorage.getItem('refresh_token'),
            });
        }

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');

                if (!refreshToken) {
                    console.log('🔴 No refresh token available, redirecting to login');
                    window.location.href = '/login';
                    return Promise.reject(error);
                }

                console.log('🔄 Attempting token refresh...');
                const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
                    refresh: refreshToken,
                });

                const { access } = response.data;
                localStorage.setItem('access_token', access);
                console.log('✅ Token refreshed successfully');

                originalRequest.headers.Authorization = `Bearer ${access}`;
                return api(originalRequest);
            } catch (refreshError) {
                // Refresh failed, logout user
                console.log('🔴 Token refresh failed:', refreshError);
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

// Auth API
export const authAPI = {
    register: (data: { username: string; email: string; password: string }) =>
        api.post('/onboarding/register/', data),
    login: (data: { username: string; password: string }) =>
        api.post('/auth/login/', data),
    refresh: (refresh: string) =>
        api.post('/auth/refresh/', { refresh }),
};

// Onboarding API
export const onboardingAPI = {
    getLanguages: () => api.get('/onboarding/languages/'),
    getOptions: () => api.get('/onboarding/options/'),
    getSteps: () => api.get('/onboarding/steps/'),
    getProgress: () => api.get('/onboarding/progress/'),
    completeStep: (stepType: string, data: Record<string, unknown>) =>
        api.post('/onboarding/complete-step/', { step_type: stepType, data }),
    getVAKQuestions: () => api.get('/onboarding/vak-assessment/'),
    submitVAK: (answers: Array<{ question_order: number; answer: string }>) =>
        api.post('/onboarding/submit-vak/', { answers }),
    complete: () => api.post('/onboarding/complete/'),
};

// Users API (fully typed)
export const usersAPI = {
    /** Get current user profile */
    getMe: () => api.get<User>('/users/me/'),

    /** Update current user profile */
    updateMe: (data: Partial<User>) => api.patch<User>('/users/me/', data),

    /** Delete current user account */
    deleteMe: () => api.delete('/users/me/'),

    /** Get dashboard stats */
    getDashboard: () => api.get<DashboardData>('/users/me/dashboard/'),

    /** Record a study session */
    recordSession: (data: RecordSessionRequest) =>
        api.post<RecordSessionResponse>('/users/me/record-session/', data),

    /** Get activity history */
    getActivity: (days: number = 30) =>
        api.get<ActivityHistoryResponse>(`/users/me/activity/?days=${days}`),

    /** Get streak details */
    getStreaks: () => api.get<StreakDetailResponse>('/users/me/streaks/'),

    /** Get XP history */
    getXPHistory: (days: number = 7) =>
        api.get<XPHistoryResponse>(`/users/me/xp-history/?days=${days}`),

    /** Get user settings */
    getSettings: () => api.get<UserSettings>('/users/me/settings/'),

    /** Update user settings */
    updateSettings: (data: Partial<UserSettings>) =>
        api.patch<UserSettings>('/users/me/settings/', data),
};

// World API (future)
export const worldAPI = {
    getWorlds: () => api.get('/worlds/'),
    getWorld: (id: number) => api.get(`/worlds/${id}/`),
    getRooms: (worldId: number) => api.get(`/worlds/${worldId}/rooms/`),
};

// Recommendations API (ARIA)
export const recommendationsAPI = {
    getRecommended: (limit: number = 10) => api.get(`/recommendations/scenarios/?limit=${limit}`),
    getSimilar: (scenarioId: number, limit: number = 5) => api.get(`/recommendations/similar/${scenarioId}/?limit=${limit}`),
};

// Progress API
export const progressAPI = {
    getMyProgress: () => api.get('/progress/'),
    getScenarioProgress: (slug: string) => api.get(`/progress/scenario/${slug}/`),
    getPendingMilestones: (slug: string) => api.get(`/progress/scenario/${slug}/pending/`),
    getNextMilestone: (slug: string) => api.get(`/progress/scenario/${slug}/next/`),
    getMilestoneDetail: (id: number) => api.get(`/progress/milestone/${id}/`),
    startMilestone: (milestoneId: number) => api.post('/progress/start/', { milestone_id: milestoneId }),
    completeMilestone: (milestoneId: number, score: number = 100, timeSpent: number = 0) =>
        api.post('/progress/complete/', {
            milestone_id: milestoneId,
            score,
            time_spent_seconds: timeSpent
        }),
};

// Orchestrator API (Intent-First Learning)
export const orchestratorAPI = {
    // Get all scenarios
    getScenarios: () => api.get('/scenarios/'),

    // Get scenario with milestones and progress
    getScenarioProgress: (slug: string) => api.get(`/scenarios/${slug}/progress/`),

    // Get learning content for a milestone (uses orchestrator)
    getMilestoneContent: (milestoneId: number) => api.get(`/milestones/${milestoneId}/content/`),

    // Start a milestone
    startMilestone: (milestoneId: number) => api.post(`/milestones/${milestoneId}/start/`),

    // Complete an intent
    completeIntent: (intentId: number, data: Record<string, unknown>) => api.post(`/intents/${intentId}/complete/`, data),

    // Get user's overall progress
    getUserProgress: () => api.get('/progress/'),
};

export default api;

