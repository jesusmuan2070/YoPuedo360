/**
 * Auth Context - Manages authentication state
 */

import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        // Check for existing token on mount
        const token = localStorage.getItem('access_token');
        if (token) {
            setIsAuthenticated(true);
            // TODO: Fetch user profile
        }
        setLoading(false);
    }, []);

    const register = async (email, username, password) => {
        try {
            const response = await authAPI.register({
                email,
                username,
                password,
                password_confirm: password,
            });

            const { user: userData, tokens } = response.data;

            localStorage.setItem('access_token', tokens.access);
            localStorage.setItem('refresh_token', tokens.refresh);

            setUser(userData);
            setIsAuthenticated(true);

            return { success: true, data: response.data };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data || { message: 'Registration failed' }
            };
        }
    };

    const login = async (username, password) => {
        try {
            const response = await authAPI.login({ username, password });

            const { access, refresh } = response.data;

            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);

            setIsAuthenticated(true);

            return { success: true };
        } catch (error) {
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
