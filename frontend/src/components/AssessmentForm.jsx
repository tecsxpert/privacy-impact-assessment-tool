import { useState } from 'react';

export default function AssessmentForm({ initial = {}, onSubmit, loading }) {
  const [form, setForm] = useState({
    title:             initial.title             || '',
    description:       initial.description       || '',
    projectName:       initial.projectName       || '',
    dataTypes:         initial.dataTypes         || '',
    dataSubjects:      initial.dataSubjects      || '',
    processingPurpose: initial.processingPurpose || '',
    riskLevel:         initial.riskLevel         || 'LOW',
    status:            initial.status            || 'DRAFT',
    privacyScore:      initial.privacyScore      || '',
    deadline:          initial.deadline          || '',
  });

  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!form.title.trim())
      newErrors.title = 'Title is required';
    if (!form.projectName.trim())
      newErrors.projectName = 'Project name is required';
    if (form.privacyScore &&
       (form.privacyScore < 0 || form.privacyScore > 100))
      newErrors.privacyScore = 'Score must be 0-100';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: '' }));
  };

  const handleSubmit = () => {
    if (validate()) onSubmit(form);
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      {/* Title */}
      <div className="mb-4">
        <label className="block text-gray-700 font-medium mb-1 text-sm">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          type="text" name="title" value={form.title}
          onChange={handleChange} placeholder="Enter assessment title"
          className={`w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${errors.title ? 'border-red-500' : 'border-gray-300'}`}
        />
        {errors.title && <p className="text-red-500 text-xs mt-1">{errors.title}</p>}
      </div>

      {/* Project Name */}
      <div className="mb-4">
        <label className="block text-gray-700 font-medium mb-1 text-sm">
          Project Name <span className="text-red-500">*</span>
        </label>
        <input
          type="text" name="projectName" value={form.projectName}
          onChange={handleChange} placeholder="Enter project name"
          className={`w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${errors.projectName ? 'border-red-500' : 'border-gray-300'}`}
        />
        {errors.projectName && <p className="text-red-500 text-xs mt-1">{errors.projectName}</p>}
      </div>

      {/* Description */}
      <div className="mb-4">
        <label className="block text-gray-700 font-medium mb-1 text-sm">Description</label>
        <textarea
          name="description" value={form.description}
          onChange={handleChange} rows={3} placeholder="Describe the assessment"
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Data Types */}
      <div className="mb-4">
        <label className="block text-gray-700 font-medium mb-1 text-sm">Data Types</label>
        <input
          type="text" name="dataTypes" value={form.dataTypes}
          onChange={handleChange} placeholder="e.g. email, location, health"
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Data Subjects */}
      <div className="mb-4">
        <label className="block text-gray-700 font-medium mb-1 text-sm">Data Subjects</label>
        <input
          type="text" name="dataSubjects" value={form.dataSubjects}
          onChange={handleChange} placeholder="e.g. Employees, Customers"
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Processing Purpose */}
      <div className="mb-4">
        <label className="block text-gray-700 font-medium mb-1 text-sm">Processing Purpose</label>
        <textarea
          name="processingPurpose" value={form.processingPurpose}
          onChange={handleChange} rows={2}
          placeholder="Why is this data being processed?"
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Risk Level and Status */}
      <div className="mb-4 grid grid-cols-2 gap-4">
        <div>
          <label className="block text-gray-700 font-medium mb-1 text-sm">Risk Level</label>
          <select name="riskLevel" value={form.riskLevel} onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="LOW">Low</option>
            <option value="MEDIUM">Medium</option>
            <option value="HIGH">High</option>
            <option value="CRITICAL">Critical</option>
          </select>
        </div>
        <div>
          <label className="block text-gray-700 font-medium mb-1 text-sm">Status</label>
          <select name="status" value={form.status} onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="DRAFT">Draft</option>
            <option value="IN_REVIEW">In Review</option>
            <option value="APPROVED">Approved</option>
            <option value="REJECTED">Rejected</option>
          </select>
        </div>
      </div>

      {/* Score and Deadline */}
      <div className="mb-6 grid grid-cols-2 gap-4">
        <div>
          <label className="block text-gray-700 font-medium mb-1 text-sm">Privacy Score (0-100)</label>
          <input
            type="number" name="privacyScore" value={form.privacyScore}
            onChange={handleChange} min="0" max="100" placeholder="0-100"
            className={`w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${errors.privacyScore ? 'border-red-500' : 'border-gray-300'}`}
          />
          {errors.privacyScore && <p className="text-red-500 text-xs mt-1">{errors.privacyScore}</p>}
        </div>
        <div>
          <label className="block text-gray-700 font-medium mb-1 text-sm">Deadline</label>
          <input
            type="date" name="deadline" value={form.deadline}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Submit Button */}
      <button
        onClick={handleSubmit} disabled={loading}
        className="w-full bg-blue-800 text-white py-3 rounded-lg hover:bg-blue-900 disabled:opacity-50 font-semibold text-sm"
      >
        {loading ? 'Saving...' : 'Save Assessment'}
      </button>
    </div>
  );
}