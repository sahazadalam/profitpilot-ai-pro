import { api } from '@/services/api';

export const dashboardApi = {
  async getDashboard() {
    const response = await api.get('/dashboard');
    return response.data.data;
  },

  async getRevenueChart() {
    const response = await api.get('/dashboard/revenue-chart');
    return response.data.data;
  },

  async getTopProducts() {
    const response = await api.get('/dashboard/top-products');
    return response.data.data;
  },

  async getRecentSales() {
    const response = await api.get('/dashboard/recent-sales');
    return response.data.data;
  },

  async getProfitSummary() {
    const response = await api.get('/dashboard/profit-summary');
    return response.data.data;
  },
};
