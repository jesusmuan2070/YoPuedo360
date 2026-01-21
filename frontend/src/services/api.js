/**
 * API Service for YoPuedo360
 * Handles all HTTP requests to the backend
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with defaults
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
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

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
                    refresh: refreshToken,
                });

                const { access } = response.data;
                localStorage.setItem('access_token', access);

                originalRequest.headers.Authorization = `Bearer ${access}`;
                return api(originalRequest);
            } catch (refreshError) {
                // Refresh failed, logout user
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
    register: (data) => api.post('/onboarding/register/', data),
    login: (data) => api.post('/auth/login/', data),
    refresh: (refresh) => api.post('/auth/refresh/', { refresh }),
};

// Onboarding API
export const onboardingAPI = {
    getLanguages: () => api.get('/onboarding/languages/'),
    getOptions: () => api.get('/onboarding/options/'),  // Goals, interests, work_domains from DB
    getSteps: () => api.get('/onboarding/steps/'),
    getProgress: () => api.get('/onboarding/progress/'),
    completeStep: (stepType, data) => api.post('/onboarding/complete-step/', { step_type: stepType, data }),
    getVAKQuestions: () => api.get('/onboarding/vak-assessment/'),
    submitVAK: (answers) => api.post('/onboarding/submit-vak/', { answers }),
    complete: () => api.post('/onboarding/complete/'),
};

// Profile API (future)
export const profileAPI = {
    getProfile: () => api.get('/users/me/profile/'),
    updateProfile: (data) => api.patch('/users/me/profile/', data),
};

// World API (future)
export const worldAPI = {
    getWorlds: () => api.get('/worlds/'),
    getWorld: (id) => api.get(`/worlds/${id}/`),
    getRooms: (worldId) => api.get(`/worlds/${worldId}/rooms/`),
};

// Recommendations API (ARIA)
export const recommendationsAPI = {
    getRecommended: (limit = 10) => api.get(`/recommendations/scenarios/?limit=${limit}`),
    getSimilar: (scenarioId, limit = 5) => api.get(`/recommendations/similar/${scenarioId}/?limit=${limit}`),
};

// Progress API
export const progressAPI = {
    getMyProgress: () => api.get('/progress/'),
    getScenarioProgress: (slug) => api.get(`/progress/scenario/${slug}/`),
    getPendingMilestones: (slug) => api.get(`/progress/scenario/${slug}/pending/`),
    getNextMilestone: (slug) => api.get(`/progress/scenario/${slug}/next/`),
    getMilestoneDetail: (id) => api.get(`/progress/milestone/${id}/`),
    startMilestone: (milestoneId) => api.post('/progress/start/', { milestone_id: milestoneId }),
    completeMilestone: (milestoneId, score = 100, timeSpent = 0) =>
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
    getScenarioProgress: (slug) => api.get(`/scenarios/${slug}/progress/`),

    // Get learning content for a milestone (uses orchestrator)
    getMilestoneContent: (milestoneId) => api.get(`/milestones/${milestoneId}/content/`),

    // Start a milestone
    startMilestone: (milestoneId) => api.post(`/milestones/${milestoneId}/start/`),

    // Complete an intent
    completeIntent: (intentId, data) => api.post(`/intents/${intentId}/complete/`, data),

    // Get user's overall progress
    getUserProgress: () => api.get('/progress/'),
};

export default api;
