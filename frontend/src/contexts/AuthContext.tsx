import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { authService } from '@/services/auth';
import { User } from '@/types';
import toast from 'react-hot-toast';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  isAdmin: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: { full_name: string; email: string; password: string }) => Promise<void>;
  logout: () => void;
  updateUser: (user: User) => void;
  isDemoMode: boolean;
  enterDemoMode: () => void;
  exitDemoMode: () => void;
}

const DEMO_USER: User = {
  id: 'demo_001',
  full_name: 'Demo User',
  email: 'demo@profitpilot.com',
  role: 'admin',
  is_active: true,
  created_at: new Date().toISOString(),
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isDemoMode, setIsDemoMode] = useState(false);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const storedUser = localStorage.getItem('user');
        const token = localStorage.getItem('access_token');
        const demo = localStorage.getItem('demo_mode');
        
        if (demo === 'true') {
          setIsDemoMode(true);
          setUser(DEMO_USER);
        } else if (storedUser && token) {
          const parsedUser = JSON.parse(storedUser);
          // Ensure user has admin role for full access
          parsedUser.role = 'admin';
          setUser(parsedUser);
        }
      } catch (error) {
        console.error('Failed to load user:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadUser();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await authService.login({ email, password });
      
      if (response.access_token) {
        localStorage.setItem('access_token', response.access_token);
        localStorage.removeItem('demo_mode');
        setIsDemoMode(false);
        
        try {
          const userData = await authService.getCurrentUser();
          // Grant admin role to all users
          userData.role = 'admin';
          setUser(userData);
          localStorage.setItem('user', JSON.stringify(userData));
          toast.success('Welcome back!');
        } catch (error) {
          console.error('Failed to get user profile:', error);
          // Create fallback user with admin role
          const fallbackUser: User = {
            id: 'user_001',
            full_name: email.split('@')[0] || 'User',
            email: email,
            role: 'admin',
            is_active: true,
            created_at: new Date().toISOString(),
          };
          setUser(fallbackUser);
          localStorage.setItem('user', JSON.stringify(fallbackUser));
          toast.success('Welcome!');
        }
      }
    } catch (error) {
      console.error('Login error:', error);
      toast.error('Login failed. Please try again.');
      throw error;
    }
  };

  const register = async (data: { full_name: string; email: string; password: string }) => {
    try {
      await authService.register(data);
      toast.success('Account created successfully! Please login.');
    } catch (error) {
      console.error('Registration error:', error);
      toast.error('Registration failed. Please try again.');
      throw error;
    }
  };

  const logout = useCallback(() => {
    authService.logout();
    localStorage.removeItem('demo_mode');
    setIsDemoMode(false);
    setUser(null);
    toast.success('Logged out successfully');
    window.location.href = '/';
  }, []);

  const updateUser = useCallback((updatedUser: User) => {
    setUser(updatedUser);
    localStorage.setItem('user', JSON.stringify(updatedUser));
  }, []);

  const enterDemoMode = useCallback(() => {
    setIsDemoMode(true);
    setUser(DEMO_USER);
    localStorage.setItem('demo_mode', 'true');
    localStorage.setItem('user', JSON.stringify(DEMO_USER));
    toast.success('Entered demo mode');
  }, []);

  const exitDemoMode = useCallback(() => {
    setIsDemoMode(false);
    setUser(null);
    localStorage.removeItem('demo_mode');
    localStorage.removeItem('user');
    window.location.href = '/';
  }, []);

  // Grant admin access to all users
  const isAdmin = true;

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user || isDemoMode,
        isAdmin,
        login,
        register,
        logout,
        updateUser,
        isDemoMode,
        enterDemoMode,
        exitDemoMode,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
