export interface RevenueAnalytics {
  today: number;
  weekly: number;
  monthly: number;
  yearly: number;
  total: number;
}

export interface ProfitAnalytics {
  today: number;
  weekly: number;
  monthly: number;
  yearly: number;
  total: number;
}

export interface BusinessHealth {
  score: number;
  status: string;
  explanation: string;
  details: {
    revenue_growth: number;
    profit_margin: number;
    inventory_health: number;
    sales_trend: string;
    low_stock_ratio: number;
  };
}

export interface KPIs {
  revenue: number;
  profit: number;
  sales: number;
  orders: number;
  products: number;
  average_order_value: number;
  average_profit_per_sale: number;
}

export interface Insight {
  type: 'positive' | 'negative' | 'neutral' | 'warning' | 'critical';
  category: string;
  message: string;
  priority: 'high' | 'medium' | 'low';
}

export interface TrendData {
  daily: {
    dates: string[];
    revenue: number[];
    profit: number[];
  };
  weekly: {
    periods: string[];
    revenue: number[];
    profit: number[];
  };
  monthly: {
    periods: string[];
    revenue: number[];
    profit: number[];
  };
}

export interface CategoryData {
  data: Array<{
    category: string;
    total_sale_amount: number;
    profit: number;
    quantity: number;
  }>;
  best_category: {
    name: string;
    revenue: number;
    profit: number;
  };
  worst_category: {
    name: string;
    revenue: number;
    profit: number;
  };
}

