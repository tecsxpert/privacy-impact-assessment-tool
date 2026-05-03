// src/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import ListPage from './pages/ListPage';
import CreateEditPage from './pages/CreateEditPage';
import DashboardPage from './pages/DashboardPage';
import DetailPage from './pages/DetailPage';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={
            <ProtectedRoute><DashboardPage /></ProtectedRoute>
          } />
          <Route path="/dashboard" element={
            <ProtectedRoute><DashboardPage /></ProtectedRoute>
          } />
          <Route path="/assessments" element={
            <ProtectedRoute><ListPage /></ProtectedRoute>
          } />
          <Route path="/assessments/create" element={
            <ProtectedRoute><CreateEditPage /></ProtectedRoute>
          } />
          <Route path="/assessments/edit/:id" element={
            <ProtectedRoute><CreateEditPage /></ProtectedRoute>
          } />
          <Route path="/assessments/:id" element={
            <ProtectedRoute><DetailPage /></ProtectedRoute>
          } />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;