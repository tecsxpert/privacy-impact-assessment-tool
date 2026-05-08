// src/components/SearchFilterBar.jsx
import { useState, useEffect } from 'react';

export default function SearchFilterBar({ onSearch }) {
  const [query, setQuery]       = useState('');
  const [status, setStatus]     = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo]     = useState('');

  // Debounce — waits 400ms after user stops typing
  useEffect(() => {
    const timer = setTimeout(() => {
      onSearch({ query, status, dateFrom, dateTo });
    }, 400);
    return () => clearTimeout(timer);
  }, [query, status, dateFrom, dateTo]);

  const handleClear = () => {
    setQuery('');
    setStatus('');
    setDateFrom('');
    setDateTo('');
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 mb-6">
      <div className="flex flex-wrap gap-3 items-end">

        {/* Search Input */}
        <div className="flex-1 min-w-48">
          <label className="block text-xs text-gray-500 mb-1">
            Search
          </label>
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search by title or project..."
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Status Dropdown */}
        <div className="min-w-36">
          <label className="block text-xs text-gray-500 mb-1">
            Status
          </label>
          <select
            value={status}
            onChange={e => setStatus(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Statuses</option>
            <option value="DRAFT">Draft</option>
            <option value="IN_REVIEW">In Review</option>
            <option value="APPROVED">Approved</option>
            <option value="REJECTED">Rejected</option>
          </select>
        </div>

        {/* Date From */}
        <div className="min-w-36">
          <label className="block text-xs text-gray-500 mb-1">
            From Date
          </label>
          <input
            type="date"
            value={dateFrom}
            onChange={e => setDateFrom(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Date To */}
        <div className="min-w-36">
          <label className="block text-xs text-gray-500 mb-1">
            To Date
          </label>
          <input
            type="date"
            value={dateTo}
            onChange={e => setDateTo(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Clear Button */}
        <button
          onClick={handleClear}
          className="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50"
        >
          Clear
        </button>
      </div>
    </div>
  );
}