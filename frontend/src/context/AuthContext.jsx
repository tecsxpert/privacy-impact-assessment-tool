// src/context/AuthContext.jsx
import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem('jwt');
    return token ? { token } : null;
  });

  const login = (token) => {
    localStorage.setItem('jwt', token);
    setUser({ token });
  };

  const logout = () => {
    localStorage.removeItem('jwt');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}