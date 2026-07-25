export interface DashboardData {
  total_products: number;
  total_sales: number;
  today_sales: number;
  revenue: number;
  profit: number;
  inventory_value: number;
  out_of_stock: number;
  low_stock: number;
  health_score: number;
  top_products: TopProduct[];
  recent_sales: RecentSale[];
  revenue_data: ChartData[];
  profit_data: ChartData[];
}

export interface TopProduct {
  product_id: string;
  product_name: string;
  category: string;
  total_quantity_sold: number;
  total_revenue: number;
  total_profit: number;
}

export interface RecentSale {
  id: string;
  invoice_number: string;
  product_name: string;
  customer_name: string;
  total_sale_amount: number;
  sale_date: string;
}

export interface ChartData {
  date: string;
  revenue: number;
  profit: number;
}

