import { api } from '@/services/api';
import {
  RestockRecommendation,
  PricingRecommendation,
  LossProduct,
  BundleRecommendation,
  PerformanceScore,
  BusinessRisk,
  Optimization
} from '@/types/recommendations';

export const recommendationsService = {
  async getRestockRecommendations(): Promise<RestockRecommendation[]> {
    const response = await api.get('/recommend/restock');
    return response.data.data;
  },

  async getPricingRecommendations(): Promise<PricingRecommendation[]> {
    const response = await api.get('/recommend/pricing');
    return response.data.data;
  },

  async getDeadStock(): Promise<any[]> {
    const response = await api.get('/recommend/dead-stock');
    return response.data.data;
  },

  async getLossProducts(): Promise<LossProduct[]> {
    const response = await api.get('/recommend/loss-products');
    return response.data.data;
  },

  async getBundles(): Promise<BundleRecommendation[]> {
    const response = await api.get('/recommend/bundles');
    return response.data.data;
  },

  async getPerformanceScores(): Promise<PerformanceScore[]> {
    const response = await api.get('/recommend/performance');
    return response.data.data;
  },

  async getBusinessRisk(): Promise<BusinessRisk> {
    const response = await api.get('/recommend/business-risk');
    return response.data.data;
  },

  async getOptimizations(): Promise<Optimization[]> {
    const response = await api.get('/recommend/optimization');
    return response.data.data;
  },

  async getExecutiveSummary(): Promise<any> {
    const response = await api.get('/recommend/executive-summary');
    return response.data.data;
  }
};
