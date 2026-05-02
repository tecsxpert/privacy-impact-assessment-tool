// src/components/AssessmentTable.jsx
export default function AssessmentTable({ assessments, onView }) {
  return (
    <div className="overflow-x-auto rounded shadow">
      <table className="min-w-full bg-white border border-gray-200">
        <thead className="bg-blue-800 text-white">
          <tr>
            <th className="px-4 py-3 text-left text-sm font-semibold">#</th>
            <th className="px-4 py-3 text-left text-sm font-semibold">Title</th>
            <th className="px-4 py-3 text-left text-sm font-semibold">Project</th>
            <th className="px-4 py-3 text-left text-sm font-semibold">Risk Level</th>
            <th className="px-4 py-3 text-left text-sm font-semibold">Status</th>
            <th className="px-4 py-3 text-left text-sm font-semibold">Score</th>
            <th className="px-4 py-3 text-left text-sm font-semibold">Actions</th>
          </tr>
        </thead>
        <tbody>
          {assessments.map((item, index) => (
            <tr
              key={item.id}
              className="border-t border-gray-200 hover:bg-gray-50"
            >
              <td className="px-4 py-3 text-sm text-gray-600">
                {index + 1}
              </td>
              <td className="px-4 py-3 text-sm font-medium text-gray-800">
                {item.title}
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">
                {item.projectName}
              </td>
              <td className="px-4 py-3 text-sm">
                <RiskBadge level={item.riskLevel} />
              </td>
              <td className="px-4 py-3 text-sm">
                <StatusBadge status={item.status} />
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">
                {item.privacyScore != null ? `${item.privacyScore}/100` : '—'}
              </td>
              <td className="px-4 py-3 text-sm">
                <button
                  onClick={() => onView(item.id)}
                  className="text-blue-700 hover:underline font-medium"
                >
                  View
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function RiskBadge({ level }) {
  const colors = {
    LOW:      'bg-green-100 text-green-800',
    MEDIUM:   'bg-yellow-100 text-yellow-800',
    HIGH:     'bg-orange-100 text-orange-800',
    CRITICAL: 'bg-red-100 text-red-800',
  };
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${colors[level] || 'bg-gray-100 text-gray-800'}`}>
      {level}
    </span>
  );
}

function StatusBadge({ status }) {
  const colors = {
    DRAFT:     'bg-gray-100 text-gray-800',
    IN_REVIEW: 'bg-blue-100 text-blue-800',
    APPROVED:  'bg-green-100 text-green-800',
    REJECTED:  'bg-red-100 text-red-800',
  };
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${colors[status] || 'bg-gray-100 text-gray-800'}`}>
      {status}
    </span>
  );
}