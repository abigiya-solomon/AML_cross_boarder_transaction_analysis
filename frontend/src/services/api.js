import axios from 'axios';

// Resolves backend API URL whether user set VITE_API_URL with or without '/api' or trailing slash
let rawBaseUrl = (import.meta.env.VITE_API_URL || '/api').trim();
if (rawBaseUrl.endsWith('/')) {
  rawBaseUrl = rawBaseUrl.slice(0, -1);
}
if (rawBaseUrl.startsWith('http') && !rawBaseUrl.endsWith('/api')) {
  rawBaseUrl = `${rawBaseUrl}/api`;
}

const API_BASE = rawBaseUrl;

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => {
  const res = await client.get('/health');
  return res.data;
};

export const getDashboardStats = async () => {
  const res = await client.get('/dashboard/stats');
  return res.data;
};

export const getTransactions = async (params = {}) => {
  const res = await client.get('/transactions', { params });
  return res.data;
};

export const getTransactionDetail = async (id) => {
  const res = await client.get(`/transactions/${id}`);
  return res.data;
};

export const predictSingle = async (data) => {
  const res = await client.post('/predict', data);
  return res.data;
};

export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await client.post('/predict/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return res.data;
};

export const getModelInfo = async () => {
  const res = await client.get('/model/info');
  return res.data;
};
