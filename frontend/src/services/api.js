// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8080/api',
  timeout: 15000,
});

// Attach JWT token to every request
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('jwt');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Handle responses globally
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('jwt');
      localStorage.removeItem('username');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Assessment API
export const assessmentApi = {
  getAll: (page = 0, size = 10) =>
    api.get(`/assessments/all?page=${page}&size=${size}`),
  getById: (id) =>
    api.get(`/assessments/${id}`),
  create: (data) =>
    api.post('/assessments/create', data),
  update: (id, data) =>
    api.put(`/assessments/${id}`, data),
  delete: (id) =>
    api.delete(`/assessments/${id}`),
  search: (q = '', status = '', page = 0) =>
    api.get(`/assessments/search?q=${q}&status=${status}&page=${page}`),
  exportCsv: () =>
    api.get('/assessments/export', { responseType: 'blob' }),
  getStats: () =>
    api.get('/assessments/stats'),
};

// Auth API
export const authApi = {
  login:    (creds) => api.post('/auth/login', creds),
  register: (data)  => api.post('/auth/register', data),
};

export default api;