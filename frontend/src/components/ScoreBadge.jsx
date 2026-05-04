// src/components/ScoreBadge.jsx
export default function ScoreBadge({ score, riskLevel }) {
  const getColor = () => {
    if (score >= 80) return 'bg-green-100 text-green-800';
    if (score >= 60) return 'bg-yellow-100 text-yellow-800';
    if (score >= 40) return 'bg-orange-100 text-orange-800';
    return 'bg-red-100 text-red-800';
  };

  const getRiskColor = () => {
    const colors = {
      LOW:      'bg-green-100 text-green-800',
      MEDIUM:   'bg-yellow-100 text-yellow-800',
      HIGH:     'bg-orange-100 text-orange-800',
      CRITICAL: 'bg-red-100 text-red-800',
    };
    return colors[riskLevel] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="flex gap-2 items-center">
      {score != null && (
        <span className={`px-3 py-1 rounded-full text-sm font-bold ${getColor()}`}>
          Score: {score}/100
        </span>
      )}
      {riskLevel && (
        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getRiskColor()}`}>
          {riskLevel}
        </span>
      )}
    </div>
  );
}