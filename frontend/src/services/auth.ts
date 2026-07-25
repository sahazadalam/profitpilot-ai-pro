import { api } from './api';
import { User, LoginCredentials, RegisterCredentials, AuthResponse } from '@/types';
import toast from 'react-hot-toast';

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      console.log('🔐 Attempting login:', credentials.email);
      const response = await api.post('/auth/login', credentials);
      console.log('✅ Login successful:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('❌ Login error:', error);
      
      // Extract error message from response
      const errorMessage = error.response?.data?.error?.message || 
                          error.response?.data?.message || 
                          error.message || 
                          'Login failed. Please try again.';
      
      toast.error(errorMessage);
      throw new Error(errorMessage);
    }
  },

  async register(data: RegisterCredentials): Promise<AuthResponse> {
    try {
      console.log('📝 Attempting registration:', data.email);
      const response = await api.post('/auth/signup', data);
      console.log('✅ Registration successful:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('❌ Registration error:', error);
      
      const errorMessage = error.response?.data?.error?.message || 
                          error.response?.data?.message || 
                          error.message || 
                          'Registration failed. Please try again.';
      
      toast.error(errorMessage);
      throw new Error(errorMessage);
    }
  },

  async getCurrentUser(): Promise<User> {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error: any) {
      console.error('❌ Get user error:', error);
      throw error;
    }
  },

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },
};
