// src/components/LoadingSpinner.jsx
export default function LoadingSpinner() {
  return (
    <div className="flex justify-center items-center py-20">
      <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-800 border-t-transparent">
      </div>
      <span className="ml-4 text-gray-600 text-lg">Loading...</span>
    </div>
  );
}