export interface DemandPrediction {
  forecast: Array<{
    date: string;
    value: number;
    lower?: number;
    upper?: number;
  }>;
  model: string;
  explanation?: string;
  details?: {
    seasonality: {
      yearly: boolean;
      weekly: boolean;
      daily: boolean;
    };
    periods: number;
  };
}

export interface RevenuePrediction {
  forecast: Array<{
    date: string;
    value: number;
    lower?: number;
    upper?: number;
  }>;
  model: string;
  explanation?: string;
}

export interface ProfitPrediction {
  forecast: Array<{
    date: string;
    value: number;
    lower?: number;
    upper?: number;
  }>;
  model: string;
  explanation?: string;
}

export interface InventoryForecast {
  data: Array<{
    product_id: string;
    product_name: string;
    category: string;
    current_stock: number;
    avg_daily_sales: number;
    days_until_depletion: number;
    depletion_date: string;
    recommended_reorder_date: string;
    reorder_quantity: number;
  }>;
  total_products: number;
}

export interface Seasonality {
  has_seasonality: boolean;
  seasonality_strength: number;
  trend_strength: number;
  peak_days: string[];
  low_days: string[];
  data_points: number;
}

export interface MovingAverage {
  data: Array<{
    date: string;
    value: number;
    moving_avg: number;
  }>;
  window: number;
  total_periods: number;
}

export interface ModelComparison {
  models: Record<string, {
    mae: number;
    rmse: number;
    r2: number;
    mape: number;
  }>;
  best_model: string;
  comparison: Array<{
    model: string;
    mae: number;
    rmse: number;
    r2: number;
    mape: number;
  }>;
}
