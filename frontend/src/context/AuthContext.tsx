/**
 * Auth Context - Manages authentication state
 */

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI, usersAPI } from '../services/api';
import type { User } from '../types';

interface AuthContextType {
    user: User | null;
    loading: boolean;
    isAuthenticated: boolean;
    register: (email: string, username: string, password: string) => Promise<{ success: boolean; data?: any; error?: any }>;
    login: (username: string, password: string) => Promise<{ success: boolean; error?: any }>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        // Check for existing token on mount
        const token = localStorage.getItem('access_token');
        if (token) {
            setIsAuthenticated(true);
            loadUser();
        } else {
            setLoading(false);
        }
    }, []);

    const loadUser = async () => {
        try {
            const response = await usersAPI.getMe();
            setUser(response.data);
        } catch (error) {
            console.error('Failed to load user:', error);
            // If fetching user fails, we might still be authenticated (e.g. valid token but API error),
            // or the token might be invalid.
            // For now, if we can't get the user, we assume the token is bad? 
            // Or just leave user as null but isAuthenticated true?
            // Let's rely on the API interceptor to handle 401s and logout.
        } finally {
            setLoading(false);
        }
    };

    const register = async (email: string, username: string, password: string) => {
        try {
            const response = await authAPI.register({
                email,
                username,
                password,
            });

            const { user: userData, tokens } = response.data;

            localStorage.setItem('access_token', tokens.access);
            localStorage.setItem('refresh_token', tokens.refresh);

            setUser(userData);
            setIsAuthenticated(true);

            return { success: true, data: response.data };
        } catch (error: any) {
            return {
                success: false,
                error: error.response?.data || { message: 'Registration failed' }
            };
        }
    };

    const login = async (username: string, password: string) => {
        try {
            const response = await authAPI.login({ username, password });

            const { access, refresh } = response.data;

            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);

            setIsAuthenticated(true);
            await loadUser();

            return { success: true };
        } catch (error: any) {
            return {
                success: false,
                error: error.response?.data || { message: 'Login failed' }
            };
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
        setIsAuthenticated(false);
    };

    const value = {
        user,
        loading,
        isAuthenticated,
        register,
        login,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}

export default AuthContext;
