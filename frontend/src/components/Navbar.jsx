// src/components/Navbar.jsx
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const navigate     = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-blue-800 text-white px-4 md:px-6 py-4 shadow">
      <div className="max-w-7xl mx-auto flex justify-between items-center">

        {/* Logo */}
        <h1
          onClick={() => navigate('/')}
          className="text-lg md:text-xl font-bold cursor-pointer"
        >
          Privacy Impact Assessment
        </h1>

        {/* Nav Links */}
        <div className="flex items-center gap-2 md:gap-4">
          <button
            onClick={() => navigate('/')}
            className="text-blue-200 hover:text-white text-xs md:text-sm hidden md:block"
          >
            Dashboard
          </button>
          <button
            onClick={() => navigate('/assessments')}
            className="text-blue-200 hover:text-white text-xs md:text-sm hidden md:block"
          >
            Assessments
          </button>
          <button
            onClick={() => navigate('/analytics')}
            className="text-blue-200 hover:text-white text-xs md:text-sm hidden md:block"
          >
            Analytics
          </button>
          <button
            onClick={() => navigate('/assessments/create')}
            className="bg-white text-blue-800 px-3 py-1.5 md:px-4 md:py-2 rounded font-semibold text-xs md:text-sm hover:bg-gray-100"
          >
            + New
          </button>
          <button
            onClick={handleLogout}
            className="text-blue-200 hover:text-white text-xs md:text-sm"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}