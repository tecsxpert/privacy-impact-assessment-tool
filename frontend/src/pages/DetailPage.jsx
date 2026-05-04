// src/pages/DetailPage.jsx
import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { assessmentApi } from '../services/api';
import ScoreBadge from '../components/ScoreBadge';
import LoadingSpinner from '../components/LoadingSpinner';
import AiPanel from '../components/AiPanel';

export default function DetailPage() {
  const { id }                      = useParams();
  const navigate                    = useNavigate();
  const [assessment, setAssessment] = useState(null);
  const [loading, setLoading]       = useState(true);
  const [error, setError]           = useState('');

  useEffect(() => {
    fetchAssessment();
  }, [id]);

  const fetchAssessment = async () => {
    setLoading(true);
    try {
      const response = await assessmentApi.getById(id);
      setAssessment(response.data);
    } catch (err) {
      setError('Assessment not found or backend not running.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(
      'Are you sure you want to delete this assessment?'
    )) return;
    try {
      await assessmentApi.delete(id);
      navigate('/assessments');
    } catch (err) {
      setError('Delete failed. Please try again.');
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Navbar */}
      <nav className="bg-blue-800 text-white px-6 py-4 shadow">
        <div className="max-w-4xl mx-auto flex items-center gap-4">
          <button
            onClick={() => navigate('/assessments')}
            className="text-blue-200 hover:text-white"
          >
            ← Back
          </button>
          <h1 className="text-xl font-bold">Assessment Details</h1>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-6 py-8">

        {/* Error */}
        {error && (
          <div className="bg-red-100 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {assessment && (
          <div>
            {/* Main Card */}
            <div className="bg-white rounded-lg shadow p-6">

              {/* Header */}
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-800">
                    {assessment.title}
                  </h2>
                  <p className="text-gray-500 mt-1">
                    {assessment.projectName}
                  </p>
                </div>
                <ScoreBadge
                  score={assessment.privacyScore}
                  riskLevel={assessment.riskLevel}
                />
              </div>

              {/* Details Grid */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <p className="text-sm text-gray-500">Status</p>
                  <p className="font-semibold">
                    {assessment.status}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Deadline</p>
                  <p className="font-semibold">
                    {assessment.deadline || 'Not set'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Data Types</p>
                  <p className="font-semibold">
                    {assessment.dataTypes || 'Not specified'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">
                    Data Subjects
                  </p>
                  <p className="font-semibold">
                    {assessment.dataSubjects || 'Not specified'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Risk Level</p>
                  <p className="font-semibold">
                    {assessment.riskLevel || 'Not set'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">
                    Privacy Score
                  </p>
                  <p className="font-semibold">
                    {assessment.privacyScore != null
                      ? `${assessment.privacyScore}/100`
                      : 'Not scored'}
                  </p>
                </div>
              </div>

              {/* Description */}
              {assessment.description && (
                <div className="mb-6">
                  <p className="text-sm text-gray-500 mb-1">
                    Description
                  </p>
                  <p className="text-gray-700">
                    {assessment.description}
                  </p>
                </div>
              )}

              {/* Processing Purpose */}
              {assessment.processingPurpose && (
                <div className="mb-6">
                  <p className="text-sm text-gray-500 mb-1">
                    Processing Purpose
                  </p>
                  <p className="text-gray-700">
                    {assessment.processingPurpose}
                  </p>
                </div>
              )}

              {/* AI Description from backend */}
              {assessment.aiDescription && (
                <div className="bg-blue-50 rounded-lg p-4 mb-6">
                  <p className="text-sm font-semibold text-blue-800 mb-2">
                    🤖 AI Description
                  </p>
                  <p className="text-gray-700 text-sm">
                    {assessment.aiDescription}
                  </p>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-3 mt-6 pt-6 border-t">
                <button
                  onClick={() =>
                    navigate(`/assessments/edit/${id}`)
                  }
                  className="bg-blue-800 text-white px-6 py-2 rounded hover:bg-blue-900"
                >
                  Edit
                </button>
                <button
                  onClick={handleDelete}
                  className="bg-red-600 text-white px-6 py-2 rounded hover:bg-red-700"
                >
                  Delete
                </button>
                <button
                  onClick={() => navigate('/assessments')}
                  className="border border-gray-300 text-gray-700 px-6 py-2 rounded hover:bg-gray-50"
                >
                  Back to List
                </button>
              </div>
            </div>

            {/* ✅ AI Panel — connects to Flask AI service */}
            <AiPanel assessmentId={id} />

          </div>
        )}
      </div>
    </div>
  );
}