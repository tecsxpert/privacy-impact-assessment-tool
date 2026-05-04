// src/pages/CreateEditPage.jsx
import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { assessmentApi } from '../services/api';
import AssessmentForm from '../components/AssessmentForm';
import LoadingSpinner from '../components/LoadingSpinner';

export default function CreateEditPage() {
  const { id }                          = useParams();
  const navigate                        = useNavigate();
  const [initial, setInitial]           = useState({});
  const [loading, setLoading]           = useState(false);
  const [fetchLoading, setFetchLoading] = useState(false);
  const [error, setError]               = useState('');
  const isEdit                          = Boolean(id);

  useEffect(() => {
    if (isEdit) {
      setFetchLoading(true);
      assessmentApi.getById(id)
        .then(res => setInitial(res.data))
        .catch(() => setError('Failed to load assessment'))
        .finally(() => setFetchLoading(false));
    }
  }, [id]);

  const handleSubmit = async (formData) => {
    setLoading(true);
    setError('');
    try {
      if (isEdit) {
        await assessmentApi.update(id, formData);
      } else {
        await assessmentApi.create(formData);
      }
      navigate('/assessments');
    } catch (err) {
      setError('Failed to save. Backend may not be running yet.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-blue-800 text-white px-6 py-4 shadow">
        <div className="max-w-3xl mx-auto flex items-center gap-4">
          <button
            onClick={() => navigate('/assessments')}
            className="text-blue-200 hover:text-white"
          >
            ← Back
          </button>
          <h1 className="text-xl font-bold">
            {isEdit ? 'Edit Assessment' : 'Create New Assessment'}
          </h1>
        </div>
      </nav>

      <div className="max-w-3xl mx-auto px-6 py-8">
        {error && (
          <div className="bg-red-100 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {fetchLoading ? (
          <LoadingSpinner />
        ) : (
          <AssessmentForm
            initial={initial}
            onSubmit={handleSubmit}
            loading={loading}
          />
        )}
      </div>
    </div>
  );
}