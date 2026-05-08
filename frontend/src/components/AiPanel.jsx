// src/components/AiPanel.jsx
import { useState } from 'react';

export default function AiPanel({ assessmentId }) {
  const [aiData, setAiData]       = useState(null);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState('');
  const [activeTab, setActiveTab] = useState('');

  const tabs = [
    { key: 'describe',        label: '🔍 Describe'  },
    { key: 'recommend',       label: '💡 Recommend' },
    { key: 'generate-report', label: '📄 Report'    },
  ];

  const callAi = async (endpoint) => {
    setLoading(true);
    setError('');
    setActiveTab(endpoint);
    setAiData(null);

    try {
      const response = await fetch(
        `http://localhost:5000/${endpoint}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ assessment_id: assessmentId })
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAiData(data);

    } catch (err) {
      setError(
        'AI service not running yet. ' +
        'Flask service starts in Week 3.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 mt-6">

      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">🤖</span>
        <h3 className="text-lg font-semibold text-gray-800">
          AI Analysis
        </h3>
      </div>

      {/* Tab Buttons */}
      <div className="flex gap-2 mb-4 flex-wrap">
        {tabs.map(tab => (
          <button
            key={tab.key}
            onClick={() => callAi(tab.key)}
            disabled={loading}
            className={`px-4 py-2 rounded-lg text-sm font-medium
              transition-colors disabled:opacity-50
              ${activeTab === tab.key
                ? 'bg-blue-800 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Loading Spinner */}
      {loading && (
        <div className="flex items-center gap-3 py-6">
          <div className="animate-spin rounded-full h-6 w-6 border-2 border-blue-800 border-t-transparent"/>
          <span className="text-sm text-gray-500">
            AI is analyzing your assessment...
          </span>
        </div>
      )}

      {/* Error Message */}
      {error && !loading && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg px-4 py-3">
          <p className="text-yellow-800 text-sm">⚠️ {error}</p>
        </div>
      )}

      {/* AI Response Card */}
      {aiData && !loading && (
        <div className="bg-blue-50 border border-blue-100 rounded-lg p-4">

          {/* Response Header */}
          <div className="flex items-center gap-2 mb-3">
            <span className="text-blue-800 font-semibold text-sm">
              AI Response
            </span>
            {aiData.is_fallback && (
              <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-0.5 rounded">
                Fallback
              </span>
            )}
          </div>

          {/* Response Content */}
          {typeof aiData === 'object' ? (
            <div className="space-y-2">
              {Object.entries(aiData).map(([key, value]) => (
                key !== 'is_fallback' && (
                  <div key={key}>
                    <p className="text-xs text-gray-500 capitalize mb-1">
                      {key.replace(/_/g, ' ')}
                    </p>
                    <p className="text-sm text-gray-700">
                      {typeof value === 'object'
                        ? JSON.stringify(value, null, 2)
                        : String(value)
                      }
                    </p>
                  </div>
                )
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-700">{String(aiData)}</p>
          )}
        </div>
      )}

      {/* Placeholder when nothing loaded */}
      {!aiData && !loading && !error && (
        <div className="text-center py-8 text-gray-400">
          <p className="text-3xl mb-2">🧠</p>
          <p className="text-sm">
            Click a button above to get AI analysis
          </p>
        </div>
      )}
    </div>
  );
}