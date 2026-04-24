// src/context/AuthContext.jsx
import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    // Check if user is already logged in from previous session
    const token = localStorage.getItem('jwt');
    const username = localStorage.getItem('username');
    return token ? { token, username } : null;
  });

  const login = (token, username) => {
    localStorage.setItem('jwt', token);
    localStorage.setItem('username', username || 'User');
    setUser({ token, username });
  };

  const logout = () => {
    localStorage.removeItem('jwt');
    localStorage.removeItem('username');
    setUser(null);
  };

  const isLoggedIn = () => {
    return user !== null && user.token !== null;
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoggedIn }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}