import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import toast from 'react-hot-toast';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://profitpilot-ai-pro-backend.onrender.com';
const API_VERSION = import.meta.env.VITE_API_VERSION || '/api/v1';

// Create axios instance with full URL
export const api = axios.create({
  baseURL: API_BASE_URL + API_VERSION,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 30000,
  withCredentials: false, // Important for CORS
});

// Log requests in development
if (import.meta.env.DEV) {
  api.interceptors.request.use(
    (config) => {
      console.log('?? API Request:', config.method?.toUpperCase(), config.url, config.data);
      return config;
    },
    (error) => Promise.reject(error)
  );
}

// Request interceptor - Add JWT token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = 'Bearer ' + token;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - Handle errors
api.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log('? API Response:', response.status, response.data);
    }
    return response;
  },
  (error: AxiosError) => {
    const status = error.response?.status;
    const data = error.response?.data as any;
    
    // Log error details
    console.error('? API Error:', {
      status,
      data,
      message: error.message,
      config: error.config,
    });
    
    // Handle specific status codes
    if (status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      // Don't redirect if on login page
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
      toast.error('Session expired. Please login again.');
    }
    
    if (status === 403) {
      toast.error('You do not have permission to perform this action.');
    }
    
    if (status === 404) {
      toast.error('Resource not found.');
    }
    
    if (status === 409) {
      toast.error(data?.error?.message || 'Conflict occurred.');
    }
    
    if (status && status >= 500) {
      toast.error('Server error. Please try again later.');
    }
    
    // Show custom error message if available
    if (data?.error?.message) {
      toast.error(data.error.message);
    }
    
    return Promise.reject(error);
  }
);

export default api;

