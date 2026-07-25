import { api } from '@/services/api';
import {
  CustomerSegment,
  Anomaly,
  SimulationRequest,
  SimulationResult,
  ExplainableAI,
  MarketTrend,
  RiskPrediction,
  AIInsight,
  ScenarioComparison
} from '@/types/business-intelligence';

export const intelligenceService = {
  async getCustomerSegments(): Promise<CustomerSegment[]> {
    const response = await api.get('/intelligence/customer-segments');
    return response.data.data;
  },

  async getAnomalies(): Promise<Anomaly[]> {
    const response = await api.get('/intelligence/anomalies');
    return response.data.data;
  },

  async simulateScenario(params: SimulationRequest): Promise<SimulationResult> {
    const response = await api.post('/intelligence/simulate', params);
    return response.data.data;
  },

  async getExplainableAI(): Promise<ExplainableAI> {
    const response = await api.get('/intelligence/explain');
    return response.data.data;
  },

  async getMarketTrends(): Promise<MarketTrend> {
    const response = await api.get('/intelligence/market-trends');
    return response.data.data;
  },

  async getRiskPrediction(): Promise<RiskPrediction> {
    const response = await api.get('/intelligence/risk-prediction');
    return response.data.data;
  },

  async getAIInsights(): Promise<AIInsight[]> {
    const response = await api.get('/intelligence/insights');
    return response.data.data;
  },

  async compareScenarios(scenarioA: any, scenarioB: any): Promise<ScenarioComparison> {
    const response = await api.post('/intelligence/compare-scenarios', {
      scenario_a: scenarioA,
      scenario_b: scenarioB
    });
    return response.data.data;
  }
};
