// src/components/ProtectedRoute.jsx
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const { user } = useAuth();

  // If no token found redirect to login
  if (!user || !user.token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}