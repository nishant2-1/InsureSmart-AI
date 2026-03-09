import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (email, password, fullName) =>
    api.post('/auth/register', { email, password, full_name: fullName }),
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
  getMe: () => api.get('/auth/me')
};

export const policyAPI = {
  getPolicies: () => api.get('/policies'),
  getPolicy: (id) => api.get(`/policies/${id}`),
  createPolicy: (data) => api.post('/policies', data),
  getClaims: (policyId) => api.get(`/policies/${policyId}/claims`),
  createClaim: (policyId, data) => api.post(`/policies/${policyId}/claims`, data)
};

export const aiAPI = {
  getPolicyRecommendations: (userInput) =>
    api.post('/ai/policy-advisor', { user_input: userInput })
};

export const systemAPI = {
  getHello: () => api.get('/hello')
};

export default api;
