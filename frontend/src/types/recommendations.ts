export interface RestockRecommendation {
  product_id: string;
  product_name: string;
  current_stock: number;
  recommended_quantity: number;
  recommended_date: string;
  priority: 'high' | 'medium' | 'low';
  reason: string;
  days_until_depletion: number;
  sales_velocity: number;
}

export interface PricingRecommendation {
  product_id: string;
  product_name: string;
  current_price: number;
  suggested_price: number;
  action: 'increase' | 'decrease' | 'keep';
  expected_revenue: number;
  expected_profit: number;
  reason: string;
}

export interface LossProduct {
  product_id: string;
  product_name: string;
  category: string;
  current_price: number;
  purchase_price: number;
  margin: number;
  total_profit: number;
  total_revenue: number;
  quantity_sold: number;
  stock: number;
  reason: string;
  recommendation: string;
}

export interface BundleRecommendation {
  bundle_name: string;
  products: string[];
  product_ids: string[];
  individual_price: number;
  bundle_price: number;
  discount_percentage: number;
  expected_profit: number;
  frequency: number;
  reason: string;
}

export interface PerformanceScore {
  product_id: string;
  product_name: string;
  category: string;
  score: number;
  metrics: {
    sales_velocity: number;
    profit_margin: number;
    growth_rate: number;
    stock_health: number;
    demand_forecast: number;
  };
}

export interface BusinessRisk {
  risk_score: number;
  risk_level: string;
  description: string;
  risk_factors: {
    inventory_risk: number;
    revenue_risk: number;
    profit_risk: number;
    concentration_risk: number;
    forecast_risk: number;
  };
  recommendations: string[];
}

export interface Optimization {
  category: string;
  message: string;
  priority: 'high' | 'medium' | 'low';
  impact: string;
}

