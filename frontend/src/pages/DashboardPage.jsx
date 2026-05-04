// src/pages/DashboardPage.jsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessmentApi } from '../services/api';
import { useAuth } from '../context/AuthContext';
import {
  BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';

export default function DashboardPage() {
  const [stats, setStats]     = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate              = useNavigate();
  const { user, logout }      = useAuth();

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const response = await assessmentApi.getStats();
      setStats(response.data);
    } catch (err) {
      // Use placeholder data if backend not running
      setStats({
        totalAssessments: 0,
        highRiskCount: 0,
        averageScore: 0,
        pendingReviews: 0
      });
    } finally {
      setLoading(false);
    }
  };

  // Chart data
  const chartData = [
    { name: 'Total', value: stats?.totalAssessments || 0 },
    { name: 'High Risk', value: stats?.highRiskCount || 0 },
    { name: 'Pending', value: stats?.pendingReviews || 0 },
    { name: 'Avg Score', value: Math.round(stats?.averageScore || 0) },
  ];

  const kpiCards = [
    {
      title: 'Total Assessments',
      value: stats?.totalAssessments || 0,
      color: 'bg-blue-50 border-blue-200',
      textColor: 'text-blue-800',
      icon: '📋'
    },
    {
      title: 'High Risk',
      value: stats?.highRiskCount || 0,
      color: 'bg-red-50 border-red-200',
      textColor: 'text-red-800',
      icon: '⚠️'
    },
    {
      title: 'Average Score',
      value: `${Math.round(stats?.averageScore || 0)}/100`,
      color: 'bg-green-50 border-green-200',
      textColor: 'text-green-800',
      icon: '📊'
    },
    {
      title: 'Pending Reviews',
      value: stats?.pendingReviews || 0,
      color: 'bg-yellow-50 border-yellow-200',
      textColor: 'text-yellow-800',
      icon: '⏳'
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-blue-800 text-white px-6 py-4 shadow">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold">Privacy Impact Assessment Tool</h1>
          <div className="flex gap-4 items-center">
            <button
              onClick={() => navigate('/assessments')}
              className="text-blue-200 hover:text-white text-sm"
            >
              All Assessments
            </button>
            <button
              onClick={() => navigate('/assessments/create')}
              className="bg-white text-blue-800 px-4 py-2 rounded text-sm font-semibold"
            >
              + New
            </button>
            <button
              onClick={() => { logout(); navigate('/login'); }}
              className="text-blue-200 hover:text-white text-sm"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h2>

        {/* 4 KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {kpiCards.map((card, index) => (
            <div
              key={index}
              className={`border rounded-lg p-6 ${card.color}`}
            >
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-sm text-gray-600 mb-1">{card.title}</p>
                  <p className={`text-3xl font-bold ${card.textColor}`}>
                    {loading ? '...' : card.value}
                  </p>
                </div>
                <span className="text-2xl">{card.icon}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Recharts Bar Chart */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Assessment Overview
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#1B4F8A" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Quick Actions
          </h3>
          <div className="flex gap-3">
            <button
              onClick={() => navigate('/assessments')}
              className="bg-blue-800 text-white px-4 py-2 rounded hover:bg-blue-900 text-sm"
            >
              View All Assessments
            </button>
            <button
              onClick={() => navigate('/assessments/create')}
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 text-sm"
            >
              Create New Assessment
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}