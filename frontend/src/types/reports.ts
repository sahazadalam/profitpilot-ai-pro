export interface ReportData {
  period: string;
  generated_at: string;
  start_date?: string;
  end_date?: string;
  report?: string;
  summary?: string;
  metrics?: {
    revenue: number;
    profit: number;
    sales: number;
    products: number;
    growth: number;
    health_score: number;
  };
}

export interface ExecutiveReport {
  generated_at: string;
  period: string;
  summary: string;
  metrics: {
    revenue: number;
    profit: number;
    sales: number;
    products: number;
    growth: number;
    health_score: number;
    profit_margin: number;
    average_order_value: number;
  };
  insights: Array<{
    type: string;
    message: string;
    priority: string;
  }>;
  recommendations: Array<{
    category: string;
    message: string;
    priority: string;
    impact: string;
  }>;
  risks: Array<{
    category: string;
    message: string;
    severity: string;
  }>;
}

export interface ReportFilter {
  dateRange: 'today' | 'week' | 'month' | 'quarter' | 'year' | 'custom';
  startDate?: string;
  endDate?: string;
  category?: string;
  department?: string;
}

export interface ExportOptions {
  format: 'csv' | 'pdf';
  includeCharts: boolean;
  includeSummary: boolean;
  includeDetails: boolean;
}

