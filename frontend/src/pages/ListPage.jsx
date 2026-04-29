// src/pages/ListPage.jsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessmentApi } from '../services/api';
import { useAuth } from '../context/AuthContext';
import AssessmentTable from '../components/AssessmentTable';
import LoadingSpinner from '../components/LoadingSpinner';
import EmptyState from '../components/EmptyState';
import Pagination from '../components/Pagination';

export default function ListPage() {
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading]         = useState(true);
  const [error, setError]             = useState('');
  const [currentPage, setCurrentPage] = useState(0);
  const [totalPages, setTotalPages]   = useState(0);
  const [totalElements, setTotalElements] = useState(0);
  const navigate                      = useNavigate();
  const { user, logout }              = useAuth();

  useEffect(() => {
    fetchAssessments(currentPage);
  }, [currentPage]);

  const fetchAssessments = async (page) => {
    setLoading(true);
    setError('');
    try {
      const response = await assessmentApi.getAll(page, 10);
      setAssessments(response.data.content || []);
      setTotalPages(response.data.totalPages || 0);
      setTotalElements(response.data.totalElements || 0);
    } catch (err) {
      if (err.response?.status === 401) {
        logout();
        navigate('/login');
      } else {
        setError('Backend not connected yet. Start Spring Boot to see data.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleView = (id) => {
    navigate(`/assessments/${id}`);
  };

  const handleCreate = () => {
    navigate('/assessments/create');
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Navigation Bar */}
      <nav className="bg-blue-800 text-white px-6 py-4 shadow">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold">
            Privacy Impact Assessment Tool
          </h1>
          <div className="flex items-center gap-4">
            <span className="text-blue-200 text-sm">
              Welcome, {user?.username || 'User'}
            </span>
            <button
              onClick={handleCreate}
              className="bg-white text-blue-800 px-4 py-2 rounded font-semibold text-sm hover:bg-gray-100"
            >
              + New Assessment
            </button>
            <button
              onClick={handleLogout}
              className="text-blue-200 hover:text-white text-sm"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">

        {/* Page Header */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">
              All Assessments
            </h2>
            {!loading && totalElements > 0 && (
              <p className="text-sm text-gray-500 mt-1">
                {totalElements} total records
              </p>
            )}
          </div>
        </div>

        {/* Error State */}
        {error && (
          <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded mb-6 text-sm">
            ⚠️ {error}
            <button
              onClick={() => fetchAssessments(currentPage)}
              className="ml-4 underline font-medium"
            >
              Retry
            </button>
          </div>
        )}

        {/* Loading State */}
        {loading && <LoadingSpinner />}

        {/* Empty State */}
        {!loading && !error && assessments.length === 0 && (
          <EmptyState
            message="No assessments found. Create your first one!"
            onAdd={handleCreate}
          />
        )}

        {/* Data Table */}
        {!loading && assessments.length > 0 && (
          <>
            <AssessmentTable
              assessments={assessments}
              onView={handleView}
            />
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
            />
          </>
        )}
      </div>
    </div>
  );
}