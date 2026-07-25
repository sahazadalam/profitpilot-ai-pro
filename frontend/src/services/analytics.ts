import { api } from '@/services/api';
import {
  RevenueAnalytics,
  ProfitAnalytics,
  BusinessHealth,
  KPIs,
  Insight,
  TrendData,
  CategoryData
} from '@/types/analytics';

export const analyticsService = {
  async getRevenue(): Promise<RevenueAnalytics> {
    const response = await api.get('/analytics/revenue');
    return response.data.data;
  },

  async getProfit(): Promise<ProfitAnalytics> {
    const response = await api.get('/analytics/profit');
    return response.data.data;
  },

  async getBusinessHealth(): Promise<BusinessHealth> {
    const response = await api.get('/analytics/business-health');
    return response.data.data;
  },

  async getKPIs(): Promise<KPIs> {
    const response = await api.get('/analytics/kpis');
    return response.data.data;
  },

  async getInsights(): Promise<Insight[]> {
    const response = await api.get('/analytics/insights');
    return response.data.data;
  },

  async getTrends(): Promise<TrendData> {
    const response = await api.get('/analytics/trends');
    return response.data.data;
  },

  async getCategories(): Promise<CategoryData> {
    const response = await api.get('/analytics/category');
    return response.data.data;
  },

  async getReport(): Promise<any> {
    const response = await api.get('/analytics/report');
    return response.data.data;
  }
};

