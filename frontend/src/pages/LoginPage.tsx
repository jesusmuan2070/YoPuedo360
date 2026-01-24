/**
 * Login Page - User authentication (Compact & Beautiful)
 */

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
    const navigate = useNavigate();
    const { login } = useAuth();

    const [formData, setFormData] = useState({ username: '', password: '' });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
        setError('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        const result = await login(formData.username, formData.password);

        if (result.success) {
            navigate('/world');
        } else {
            setError(result.error?.detail || 'Invalid credentials');
        }
        setLoading(false);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-violet-600 via-purple-600 to-indigo-700 flex items-center justify-center p-4">
            <div className="w-full max-w-sm">
                {/* Glass Card */}
                <div className="backdrop-blur-xl bg-white/95 rounded-3xl shadow-2xl p-8 border border-white/20">
                    {/* Header */}
                    <div className="text-center mb-6">
                        <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                            <span className="text-3xl">🧠</span>
                        </div>
                        <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                            Welcome Back!
                        </h1>
                        <p className="text-gray-500 text-sm mt-1">Continue your journey</p>
                    </div>

                    {/* Error */}
                    {error && (
                        <div className="bg-red-50 text-red-600 text-sm px-4 py-2 rounded-xl mb-4 text-center">
                            {error}
                        </div>
                    )}

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                className="w-full px-4 py-3 bg-gray-50 border-0 rounded-xl focus:ring-2 focus:ring-purple-500 focus:bg-white transition-all outline-none"
                                placeholder="Username or email"
                                required
                            />
                        </div>

                        <div>
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                className="w-full px-4 py-3 bg-gray-50 border-0 rounded-xl focus:ring-2 focus:ring-purple-500 focus:bg-white transition-all outline-none"
                                placeholder="Password"
                                required
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl shadow-lg shadow-purple-500/30 hover:shadow-xl hover:shadow-purple-500/40 hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? '⏳ Signing in...' : 'Sign In'}
                        </button>
                    </form>

                    {/* Links */}
                    <div className="mt-6 text-center text-sm">
                        <p className="text-gray-500">
                            Don't have an account?{' '}
                            <Link to="/register" className="text-purple-600 font-semibold hover:text-pink-600">
                                Sign up
                            </Link>
                        </p>
                    </div>
                </div>

                {/* Back link */}
                <p className="text-center text-white/70 text-sm mt-4">
                    <Link to="/onboarding" className="hover:text-white">
                        ← Back to Welcome
                    </Link>
                </p>
            </div>
        </div>
    );
}
