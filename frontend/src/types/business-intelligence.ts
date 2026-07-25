export interface CustomerSegment {
  segment_id: number;
  segment_name: string;
  customer_count: number;
  average_spend: number;
  average_orders: number;
  purchase_frequency: number;
  total_revenue: number;
  percentage: number;
}

export interface Anomaly {
  date: string;
  revenue: number;
  anomaly_type: 'spike' | 'drop' | 'outlier';
  severity: 'low' | 'medium' | 'high' | 'critical';
  expected_revenue: number;
  deviation: number;
  detection_methods: string[];
  explanation: string;
}

export interface SimulationRequest {
  scenario_type: 'price_increase' | 'price_decrease' | 'stock_increase' | 'stock_decrease';
  product_id?: string;
  percentage: number;
  days: number;
}

export interface SimulationResult {
  scenario: string;
  percentage: number;
  baseline: {
    revenue: number;
    profit: number;
    quantity: number;
  };
  projected: {
    revenue: number;
    profit: number;
    quantity: number;
  };
  impact: {
    revenue_change_percent: number;
    profit_change_percent: number;
    recommendation: string;
  };
  confidence_score: number;
}

export interface ExplainableAI {
  prediction: any;
  explanation: string;
  factors: Array<{
    name: string;
    value: string;
    impact: 'high' | 'medium' | 'low';
  }>;
  confidence: number;
  importance: Array<{
    factor: string;
    value: string;
    importance_score: number;
    weight: number;
  }>;
}

export interface MarketTrend {
  industries: Record<string, {
    industry: string;
    current_demand: number;
    expected_demand: number;
    growth_rate: number;
    risk_score: number;
    opportunity_score: number;
    demand_trend: 'increasing' | 'decreasing' | 'stable';
    risk_level: string;
    recommendation: string;
  }>;
  overall_market: {
    average_growth: number;
    average_risk: number;
    average_opportunity: number;
    market_trend: string;
    market_confidence: number;
  };
  recommendations: Array<{
    type: string;
    industry: string;
    message: string;
    priority: 'high' | 'medium' | 'low';
  }>;
}

export interface RiskPrediction {
  inventory_risk: {
    score: number;
    level: string;
    factors: string[];
    recommendations: string[];
  };
  revenue_risk: {
    score: number;
    level: string;
    factors: string[];
    recommendations: string[];
  };
  profit_risk: {
    score: number;
    level: string;
    factors: string[];
    recommendations: string[];
  };
  overall_risk: {
    score: number;
    level: string;
    recommendations: string[];
  };
}

export interface AIInsight {
  type: 'positive' | 'negative' | 'neutral' | 'warning' | 'critical';
  category: string;
  message: string;
  priority: 'high' | 'medium' | 'low';
}

export interface ScenarioComparison {
  scenario_a: {
    name: string;
    projected_revenue: number;
    projected_profit: number;
    impact: any;
  };
  scenario_b: {
    name: string;
    projected_revenue: number;
    projected_profit: number;
    impact: any;
  };
  recommendation: {
    better_scenario: string;
    reason: string;
    confidence: number;
  };
  confidence_score: number;
}
