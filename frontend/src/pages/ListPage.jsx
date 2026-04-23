// src/pages/ListPage.jsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessmentApi } from '../services/api';
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
  const navigate                      = useNavigate();

  // Fetch assessments when page loads or page number changes
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
    } catch (err) {
      setError('Failed to load assessments. Please try again.');
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

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Top Navigation Bar */}
      <nav className="bg-blue-800 text-white px-6 py-4 flex justify-between items-center shadow">
        <h1 className="text-xl font-bold">
          Privacy Impact Assessment Tool
        </h1>
        <button
          onClick={handleCreate}
          className="bg-white text-blue-800 px-4 py-2 rounded font-semibold hover:bg-gray-100"
        >
          + New Assessment
        </button>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">
            All Assessments
          </h2>
          <span className="text-sm text-gray-500">
            {!loading && `${assessments.length} records found`}
          </span>
        </div>

        {/* Error State */}
        {error && (
          <div className="bg-red-100 text-red-700 px-4 py-3 rounded mb-6">
            {error}
            <button
              onClick={() => fetchAssessments(currentPage)}
              className="ml-4 underline text-red-800"
            >
              Retry
            </button>
          </div>
        )}

        {/* Loading State */}
        {loading && <LoadingSpinner />}

        {/* Empty State */}
        {!loading && !error && assessments.length === 0 && (
          <EmptyState onAdd={handleCreate} />
        )}

        {/* Table */}
        {!loading && !error && assessments.length > 0 && (
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