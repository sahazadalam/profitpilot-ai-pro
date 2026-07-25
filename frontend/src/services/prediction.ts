import { api } from '@/services/api';
import {
  DemandPrediction,
  RevenuePrediction,
  ProfitPrediction,
  InventoryForecast,
  Seasonality,
  MovingAverage,
  ModelComparison
} from '@/types/prediction';

interface PredictionParams {
  product_id?: string;
  days?: number;
  model?: string;
}

export const predictionService = {
  async predictDemand(params: PredictionParams): Promise<DemandPrediction> {
    const response = await api.post('/predict/demand', params);
    return response.data.data;
  },

  async predictRevenue(params: PredictionParams): Promise<RevenuePrediction> {
    const response = await api.post('/predict/revenue', params);
    return response.data.data;
  },

  async predictProfit(params: PredictionParams): Promise<ProfitPrediction> {
    const response = await api.post('/predict/profit', params);
    return response.data.data;
  },

  async getInventoryForecast(): Promise<InventoryForecast> {
    const response = await api.get('/predict/inventory');
    return response.data.data;
  },

  async getSeasonality(): Promise<Seasonality> {
    const response = await api.get('/predict/seasonality');
    return response.data.data;
  },

  async getMovingAverage(window?: number): Promise<MovingAverage> {
    const response = await api.get('/predict/moving-average', { params: { window } });
    return response.data.data;
  },

  async compareModels(days?: number): Promise<ModelComparison> {
    const response = await api.get('/predict/models/compare', { params: { days } });
    return response.data.data;
  },

  async getModels(): Promise<any> {
    const response = await api.get('/predict/models');
    return response.data.data;
  },

  async evaluateModel(modelName: string): Promise<any> {
    const response = await api.get('/predict/models/evaluate', { params: { model_name: modelName } });
    return response.data.data;
  }
};

