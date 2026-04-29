// src/components/Pagination.jsx
export default function Pagination({ currentPage, totalPages, onPageChange }) {
  if (totalPages <= 1) return null;

  return (
    <div className="flex justify-center items-center gap-2 mt-6">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 0}
        className="px-4 py-2 border rounded text-sm disabled:opacity-40 hover:bg-gray-100"
      >
        Previous
      </button>

      <span className="text-sm text-gray-600">
        Page {currentPage + 1} of {totalPages}
      </span>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage >= totalPages - 1}
        className="px-4 py-2 border rounded text-sm disabled:opacity-40 hover:bg-gray-100"
      >
        Next
      </button>
    </div>
  );
}