// src/pages/LoginPage.jsx
import { useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authApi } from '../services/api';

export default function LoginPage() {
  const [email, setEmail]       = useState('');
  const [password, setPassword] = useState('');
  const [error, setError]       = useState('');
  const [loading, setLoading]   = useState(false);
  const { login, user }         = useAuth();
  const navigate                = useNavigate();

  // If already logged in go to dashboard
  if (user) {
    return <Navigate to="/" replace />;
  }

  const handleLogin = async () => {
    // Basic validation
    if (!email.trim()) {
      setError('Email is required');
      return;
    }
    if (!password.trim()) {
      setError('Password is required');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await authApi.login({ email, password });
      const token = response.data.token;
      const username = response.data.username || email;
      login(token, username);
      navigate('/');
    } catch (err) {
      if (err.response?.status === 401) {
        setError('Invalid email or password');
      } else if (err.response?.status === 400) {
        setError('Please check your email and password');
      } else {
        setError('Login failed. Backend may not be running yet.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleLogin();
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">

        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-blue-800">
            Privacy Impact Assessment Tool
          </h1>
          <p className="text-gray-500 text-sm mt-2">
            Sign in to your account
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4 text-sm">
            {error}
          </div>
        )}

        {/* Email Field */}
        <div className="mb-4">
          <label className="block text-gray-700 font-medium mb-2 text-sm">
            Email Address
          </label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter your email"
            className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Password Field */}
        <div className="mb-6">
          <label className="block text-gray-700 font-medium mb-2 text-sm">
            Password
          </label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter your password"
            className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Login Button */}
        <button
          onClick={handleLogin}
          disabled={loading}
          className="w-full bg-blue-800 text-white py-3 rounded-lg hover:bg-blue-900 disabled:opacity-50 font-semibold text-sm transition-colors"
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>

        {/* Info Note */}
        <p className="text-center text-gray-400 text-xs mt-6">
          Connect to backend on port 8080 to login
        </p>
      </div>
    </div>
  );
}