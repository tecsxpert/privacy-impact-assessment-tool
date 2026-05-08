// src/pages/AnalyticsPage.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { useAuth } from '../context/AuthContext';

export default function AnalyticsPage() {
  const navigate        = useNavigate();
  const { logout }      = useAuth();
  const [period, setPeriod] = useState('month');

  const monthlyData = [
    { name: 'Jan', assessments: 4, highRisk: 1 },
    { name: 'Feb', assessments: 6, highRisk: 2 },
    { name: 'Mar', assessments: 8, highRisk: 1 },
    { name: 'Apr', assessments: 12, highRisk: 3 },
    { name: 'May', assessments: 9, highRisk: 2 },
  ];

  const weeklyData = [
    { name: 'Mon', assessments: 2, highRisk: 0 },
    { name: 'Tue', assessments: 3, highRisk: 1 },
    { name: 'Wed', assessments: 1, highRisk: 0 },
    { name: 'Thu', assessments: 4, highRisk: 1 },
    { name: 'Fri', assessments: 2, highRisk: 0 },
  ];

  const riskData = [
    { name: 'LOW',      value: 8,  fill: '#22c55e' },
    { name: 'MEDIUM',   value: 5,  fill: '#f59e0b' },
    { name: 'HIGH',     value: 3,  fill: '#f97316' },
    { name: 'CRITICAL', value: 1,  fill: '#ef4444' },
  ];

  const statusData = [
    { name: 'DRAFT',     value: 6  },
    { name: 'IN_REVIEW', value: 4  },
    { name: 'APPROVED',  value: 5  },
    { name: 'REJECTED',  value: 2  },
  ];

  const chartData = period === 'week'
    ? weeklyData
    : monthlyData;

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Navbar */}
      <nav className="bg-blue-800 text-white px-6 py-4 shadow">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold">
            Privacy Impact Assessment Tool
          </h1>
          <div className="flex gap-4 items-center">
            <button
              onClick={() => navigate('/')}
              className="text-blue-200 hover:text-white text-sm"
            >
              Dashboard
            </button>
            <button
              onClick={() => navigate('/assessments')}
              className="text-blue-200 hover:text-white text-sm"
            >
              Assessments
            </button>
            <button
              onClick={() => {
                logout();
                navigate('/login');
              }}
              className="text-blue-200 hover:text-white text-sm"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">

        {/* Header with Period Selector */}
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-2xl font-bold text-gray-800">
            Analytics
          </h2>
          <div className="flex gap-2">
            {['week', 'month'].map(p => (
              <button
                key={p}
                onClick={() => setPeriod(p)}
                className={`px-4 py-2 rounded-lg text-sm font-medium
                  ${period === p
                    ? 'bg-blue-800 text-white'
                    : 'bg-white text-gray-600 border border-gray-300 hover:bg-gray-50'
                  }`}
              >
                {p === 'week' ? 'This Week' : 'This Month'}
              </button>
            ))}
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Total',    value: 17, color: 'text-blue-800'  },
            { label: 'High Risk', value: 4, color: 'text-red-600'   },
            { label: 'Approved', value: 5,  color: 'text-green-600' },
            { label: 'Pending',  value: 4,  color: 'text-yellow-600'},
          ].map((card, i) => (
            <div
              key={i}
              className="bg-white rounded-lg shadow p-4 text-center"
            >
              <p className="text-sm text-gray-500 mb-1">
                {card.label}
              </p>
              <p className={`text-3xl font-bold ${card.color}`}>
                {card.value}
              </p>
            </div>
          ))}
        </div>

        {/* Line Chart — Trends */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Assessment Trends
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="assessments"
                stroke="#1B4F8A"
                strokeWidth={2}
                name="Total Assessments"
                dot={{ fill: '#1B4F8A' }}
              />
              <Line
                type="monotone"
                dataKey="highRisk"
                stroke="#DC2626"
                strokeWidth={2}
                name="High Risk"
                dot={{ fill: '#DC2626' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Two Charts Side by Side */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          {/* Bar Chart — Risk Distribution */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Risk Distribution
            </h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={riskData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" name="Count">
                  {riskData.map((entry, index) => (
                    <rect key={index} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Bar Chart — Status Distribution */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Status Distribution
            </h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={statusData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar
                  dataKey="value"
                  fill="#1B4F8A"
                  name="Count"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}