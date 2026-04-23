// src/components/EmptyState.jsx
export default function EmptyState({ message, onAdd }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <div className="text-6xl mb-4">📋</div>
      <h3 className="text-xl font-semibold text-gray-700 mb-2">
        No Assessments Found
      </h3>
      <p className="text-gray-500 mb-6">
        {message || 'No privacy assessments have been created yet.'}
      </p>
      {onAdd && (
        <button
          onClick={onAdd}
          className="bg-blue-800 text-white px-6 py-2 rounded hover:bg-blue-900"
        >
          + Create First Assessment
        </button>
      )}
    </div>
  );
}