"""
Analytics Engine for business intelligence.
Uses pandas and numpy for data analysis.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
import logging

from app.utils.analytics_utils import (
    create_dataframe,
    calculate_growth,
    calculate_moving_average,
    calculate_margin,
    aggregate_by_period,
    format_currency,
    format_percentage
)
from app.ai.business_health import business_health_calculator

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """
    Analytics engine for processing business data.
    """
    
    def __init__(self):
        """Initialize the analytics engine."""
        self.sales_df = None
        self.products_df = None
        self._data_loaded = False
    
    async def load_data(self, sales_data: List[Dict], products_data: List[Dict]):
        """
        Load data into DataFrames.
        
        Args:
            sales_data: List of sales documents
            products_data: List of product documents
        """
        try:
            # Create DataFrames
            self.sales_df = create_dataframe(sales_data)
            self.products_df = create_dataframe(products_data)
            
            # Clean and prepare data
            if not self.sales_df.empty:
                self.sales_df['sale_date'] = pd.to_datetime(self.sales_df['sale_date'])
                self.sales_df['total_sale_amount'] = pd.to_numeric(self.sales_df['total_sale_amount'], errors='coerce')
                self.sales_df['profit'] = pd.to_numeric(self.sales_df['profit'], errors='coerce')
                self.sales_df['quantity'] = pd.to_numeric(self.sales_df['quantity'], errors='coerce')
                
                # Fill NaN values
                self.sales_df = self.sales_df.fillna(0)
            
            if not self.products_df.empty:
                self.products_df['stock'] = pd.to_numeric(self.products_df['stock'], errors='coerce')
                self.products_df['purchase_price'] = pd.to_numeric(self.products_df['purchase_price'], errors='coerce')
                self.products_df['minimum_stock'] = pd.to_numeric(self.products_df['minimum_stock'], errors='coerce')
                
                # Fill NaN values
                self.products_df = self.products_df.fillna(0)
            
            self._data_loaded = True
            logger.info(f"Data loaded: {len(self.sales_df)} sales, {len(self.products_df)} products")
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            self._data_loaded = False
            raise
    
    def _ensure_data_loaded(self):
        """Ensure data is loaded before analysis."""
        if not self._data_loaded:
            raise ValueError("Data not loaded. Call load_data() first.")
    
    def get_revenue_analytics(self) -> Dict[str, Any]:
        """
        Calculate revenue analytics.
        
        Returns:
            Dict: Revenue analytics data
        """
        self._ensure_data_loaded()
        
        if self.sales_df.empty:
            return self._empty_analytics("revenue")
        
        now = datetime.utcnow()
        
        # Calculate periods
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=7)
        month_start = today_start - timedelta(days=30)
        year_start = today_start - timedelta(days=365)
        
        # Filter by periods
        today_sales = self.sales_df[self.sales_df['sale_date'] >= today_start]
        week_sales = self.sales_df[self.sales_df['sale_date'] >= week_start]
        month_sales = self.sales_df[self.sales_df['sale_date'] >= month_start]
        year_sales = self.sales_df[self.sales_df['sale_date'] >= year_start]
        
        return {
            "today": float(today_sales['total_sale_amount'].sum()),
            "weekly": float(week_sales['total_sale_amount'].sum()),
            "monthly": float(month_sales['total_sale_amount'].sum()),
            "yearly": float(year_sales['total_sale_amount'].sum()),
            "total": float(self.sales_df['total_sale_amount'].sum())
        }
    
    def get_profit_analytics(self) -> Dict[str, Any]:
        """
        Calculate profit analytics.
        
        Returns:
            Dict: Profit analytics data
        """
        self._ensure_data_loaded()
        
        if self.sales_df.empty:
            return self._empty_analytics("profit")
        
        now = datetime.utcnow()
        
        # Calculate periods
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=7)
        month_start = today_start - timedelta(days=30)
        year_start = today_start - timedelta(days=365)
        
        # Filter by periods
        today_sales = self.sales_df[self.sales_df['sale_date'] >= today_start]
        week_sales = self.sales_df[self.sales_df['sale_date'] >= week_start]
        month_sales = self.sales_df[self.sales_df['sale_date'] >= month_start]
        year_sales = self.sales_df[self.sales_df['sale_date'] >= year_start]
        
        return {
            "today": float(today_sales['profit'].sum()),
            "weekly": float(week_sales['profit'].sum()),
            "monthly": float(month_sales['profit'].sum()),
            "yearly": float(year_sales['profit'].sum()),
            "total": float(self.sales_df['profit'].sum())
        }
    
    def get_growth_analytics(self) -> Dict[str, Any]:
        """
        Calculate growth analytics.
        
        Returns:
            Dict: Growth analytics data
        """
        self._ensure_data_loaded()
        
        if self.sales_df.empty or len(self.sales_df) < 2:
            return self._empty_analytics("growth")
        
        # Group by date and calculate daily totals
        daily_revenue = self.sales_df.groupby(self.sales_df['sale_date'].dt.date)['total_sale_amount'].sum()
        daily_profit = self.sales_df.groupby(self.sales_df['sale_date'].dt.date)['profit'].sum()
        
        if len(daily_revenue) < 2:
            return self._empty_analytics("growth")
        
        # Calculate growth rates
        revenue_list = daily_revenue.tolist()
        profit_list = daily_profit.tolist()
        
        # Daily growth (7-day moving average)
        revenue_7d_ma = calculate_moving_average(revenue_list, 7)
        profit_7d_ma = calculate_moving_average(profit_list, 7)
        
        # Weekly growth (compare last 7 days to previous 7 days)
        current_week_revenue = daily_revenue.tail(7).sum()
        previous_week_revenue = daily_revenue.iloc[-14:-7].sum() if len(daily_revenue) >= 14 else current_week_revenue
        
        current_week_profit = daily_profit.tail(7).sum()
        previous_week_profit = daily_profit.iloc[-14:-7].sum() if len(daily_profit) >= 14 else current_week_profit
        
        # Monthly growth (compare last 30 days to previous 30 days)
        current_month_revenue = daily_revenue.tail(30).sum()
        previous_month_revenue = daily_revenue.iloc[-60:-30].sum() if len(daily_revenue) >= 60 else current_month_revenue
        
        current_month_profit = daily_profit.tail(30).sum()
        previous_month_profit = daily_profit.iloc[-60:-30].sum() if len(daily_profit) >= 60 else current_month_profit
        
        return {
            "daily": {
                "revenue": daily_revenue.iloc[-1] if not daily_revenue.empty else 0,
                "profit": daily_profit.iloc[-1] if not daily_profit.empty else 0
            },
            "weekly_growth": {
                "revenue": float(calculate_growth(current_week_revenue, previous_week_revenue)),
                "profit": float(calculate_growth(current_week_profit, previous_week_profit))
            },
            "monthly_growth": {
                "revenue": float(calculate_growth(current_month_revenue, previous_month_revenue)),
                "profit": float(calculate_growth(current_month_profit, previous_month_profit))
            },
            "moving_averages": {
                "revenue_7d": revenue_7d_ma[-1] if revenue_7d_ma else 0,
                "profit_7d": profit_7d_ma[-1] if profit_7d_ma else 0
            }
        }
    
    def get_business_health(self) -> Dict[str, Any]:
        """
        Calculate business health score.
        
        Returns:
            Dict: Business health data
        """
        self._ensure_data_loaded()
        
        if self.sales_df.empty:
            return self._empty_analytics("business_health")
        
        # Calculate metrics
        revenue_analytics = self.get_revenue_analytics()
        profit_analytics = self.get_profit_analytics()
        growth_analytics = self.get_growth_analytics()
        
        # Calculate profit margin
        total_revenue = revenue_analytics['total']
        total_profit = profit_analytics['total']
        profit_margin = calculate_margin(total_revenue, total_revenue - total_profit)
        
        # Calculate inventory health
        inventory_health = self._calculate_inventory_health()
        
        # Calculate customer health (based on repeat purchases)
        customer_health = self._calculate_customer_health()
        
        # Calculate sales volume
        sales_volume = len(self.sales_df)
        
        # Get revenue growth
        revenue_growth = growth_analytics['weekly_growth']['revenue']
        
        # Create metrics dictionary
        metrics = {
            "revenue_growth": revenue_growth,
            "profit_margin": profit_margin,
            "inventory_health": inventory_health,
            "sales_volume": sales_volume,
            "customer_health": customer_health
        }
        
        # Calculate health score
        score, status, explanation = business_health_calculator.calculate_score(metrics)
        
        return {
            "score": score,
            "status": status,
            "explanation": explanation,
            "details": {
                "revenue_growth": round(revenue_growth, 2),
                "profit_margin": round(profit_margin, 2),
                "inventory_health": round(inventory_health, 2),
                "sales_trend": "upward" if revenue_growth > 0 else "downward",
                "low_stock_ratio": self._calculate_low_stock_ratio()
            }
        }
    
    def get_top_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top selling products.
        
        Args:
            limit: Number of products to return
            
        Returns:
            List[Dict]: Top products data
        """
        self._ensure_data_loaded()
        
        if self.sales_df.empty:
            return []
        
        # Group by product
        product_sales = self.sales_df.groupby('product_id').agg({
            'product_name': 'first',
            'category': 'first',
            'quantity': 'sum',
            'total_sale_amount': 'sum',
            'profit': 'sum'
        }).reset_index()
        
        # Sort by quantity sold
        top_products = product_sales.sort_values('quantity', ascending=False).head(limit)
        
        return top_products.to_dict('records')
    
    def get_worst_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get worst selling products.
        
        Args:
            limit: Number of products to return
            
        Returns:
            List[Dict]: Worst products data
        """
        self._ensure_data_loaded()
        
        if self.sales_df.empty:
            return []
        
        # Group by product
        product_sales = self.sales_df.groupby('product_id').agg({
            'product_name': 'first',
            'category': 'first',
            'quantity': 'sum',
            'total_sale_amount': 'sum',
            'profit': 'sum'
        }).reset_index()
        
        # Sort by quantity sold (ascending)
        worst_products = product_sales.sort_values('quantity', ascending=True).head(limit)
        
        return worst_products.to_dict('records')
    
    def get_category_analytics(self) -> Dict[str, Any]:
        """
        Get category analytics.
        
        Returns:
            Dict: Category analytics data
        """
        self._ensure_data_loaded()
        
        if self.sales_df.empty:
            return self._empty_analytics("category")
        
        # Group by category
        category_analytics = self.sales_df.groupby('category').agg({
            'total_sale_amount': 'sum',
            'profit': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        # Sort by revenue
        category_analytics = category_analytics.sort_values('total_sale_amount', ascending=False)
        
        # Find best and worst categories
        best_category = category_analytics.iloc[0] if not category_analytics.empty else None
        worst_category = category_analytics.iloc[-1] if not category_analytics.empty else None
        
        return {
            "data": category_analytics.to_dict('records'),
            "best_category": {
                "name": best_category['category'] if best_category is not None else None,
                "revenue": float(best_category['total_sale_amount']) if best_category is not None else 0,
                "profit": float(best_category['profit']) if best_category is not None else 0
            } if best_category is not None else {},
            "worst_category": {
                "name": worst_category['category'] if worst_category is not None else None,
                "revenue": float(worst_category['total_sale_amount']) if worst_category is not None else 0,
                "profit": float(worst_category['profit']) if worst_category is not None else 0
            } if worst_category is not None else {}
        }
    
    def get_inventory_analytics(self) -> Dict[str, Any]:
        """
        Get inventory analytics.
        
        Returns:
            Dict: Inventory analytics data
        """
        self._ensure_data_loaded()
        
        if self.products_df.empty:
            return self._empty_analytics("inventory")
        
        total_products = len(self.products_df)
        total_stock = self.products_df['stock'].sum()
        inventory_value = (self.products_df['stock'] * self.products_df['purchase_price']).sum()
        out_of_stock = len(self.products_df[self.products_df['stock'] == 0])
        low_stock = len(self.products_df[self.products_df['stock'] <= self.products_df['minimum_stock']])
        avg_stock = self.products_df['stock'].mean()
        
        return {
            "total_products": total_products,
            "total_stock": int(total_stock),
            "inventory_value": float(inventory_value),
            "out_of_stock": out_of_stock,
            "low_stock": low_stock,
            "average_stock": float(avg_stock),
            "stock_health": self._calculate_inventory_health()
        }
    
    def get_kpis(self) -> Dict[str, Any]:
        """
        Get key performance indicators.
        
        Returns:
            Dict: KPI data
        """
        self._ensure_data_loaded()
        
        if self.sales_df.empty:
            return self._empty_analytics("kpis")
        
        total_revenue = self.sales_df['total_sale_amount'].sum()
        total_profit = self.sales_df['profit'].sum()
        total_sales = len(self.sales_df)
        total_orders = self.sales_df['invoice_number'].nunique() if 'invoice_number' in self.sales_df.columns else total_sales
        total_products = len(self.products_df) if not self.products_df.empty else 0
        
        # Calculate averages
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        avg_profit_per_sale = total_profit / total_sales if total_sales > 0 else 0
        
        return {
            "revenue": float(total_revenue),
            "profit": float(total_profit),
            "sales": total_sales,
            "orders": total_orders,
            "products": total_products,
            "average_order_value": float(avg_order_value),
            "average_profit_per_sale": float(avg_profit_per_sale)
        }
    
    def get_trends(self) -> Dict[str, Any]:
        """
        Get trend analytics.
        
        Returns:
            Dict: Trend data
        """
        self._ensure_data_loaded()
        
        if self.sales_df.empty:
            return self._empty_analytics("trends")
        
        # Daily trend (last 30 days)
        daily_trend = self.sales_df.groupby(self.sales_df['sale_date'].dt.date).agg({
            'total_sale_amount': 'sum',
            'profit': 'sum'
        }).reset_index().tail(30)
        
        # Weekly trend (last 12 weeks)
        weekly_trend = self.sales_df.groupby(self.sales_df['sale_date'].dt.to_period('W')).agg({
            'total_sale_amount': 'sum',
            'profit': 'sum'
        }).reset_index().tail(12)
        
        # Monthly trend (last 12 months)
        monthly_trend = self.sales_df.groupby(self.sales_df['sale_date'].dt.to_period('M')).agg({
            'total_sale_amount': 'sum',
            'profit': 'sum'
        }).reset_index().tail(12)
        
        return {
            "daily": {
                "dates": daily_trend['sale_date'].astype(str).tolist() if not daily_trend.empty else [],
                "revenue": daily_trend['total_sale_amount'].tolist() if not daily_trend.empty else [],
                "profit": daily_trend['profit'].tolist() if not daily_trend.empty else []
            },
            "weekly": {
                "periods": weekly_trend['sale_date'].astype(str).tolist() if not weekly_trend.empty else [],
                "revenue": weekly_trend['total_sale_amount'].tolist() if not weekly_trend.empty else [],
                "profit": weekly_trend['profit'].tolist() if not weekly_trend.empty else []
            },
            "monthly": {
                "periods": monthly_trend['sale_date'].astype(str).tolist() if not monthly_trend.empty else [],
                "revenue": monthly_trend['total_sale_amount'].tolist() if not monthly_trend.empty else [],
                "profit": monthly_trend['profit'].tolist() if not monthly_trend.empty else []
            }
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate AI-style business report.
        
        Returns:
            Dict: Report data
        """
        self._ensure_data_loaded()
        
        if self.sales_df.empty:
            return {"report": "No data available for report generation"}
        
        # Get analytics
        revenue = self.get_revenue_analytics()
        profit = self.get_profit_analytics()
        growth = self.get_growth_analytics()
        health = self.get_business_health()
        category = self.get_category_analytics()
        inventory = self.get_inventory_analytics()
        
        # Generate report sections
        sections = []
        
        # Executive Summary
        sections.append({
            "title": "Executive Summary",
            "content": f"Business is performing with a health score of {health['score']}/100 ({health['status']}). "
                      f"Total revenue: {format_currency(revenue['total'])} with {format_currency(profit['total'])} profit."
        })
        
        # Revenue Analysis
        sections.append({
            "title": "Revenue Analysis",
            "content": f"Revenue has grown by {growth['weekly_growth']['revenue']:.1f}% this week. "
                      f"Monthly revenue: {format_currency(revenue['monthly'])}."
        })
        
        # Profit Analysis
        sections.append({
            "title": "Profit Analysis",
            "content": f"Profit margin is {health['details']['profit_margin']:.1f}%. "
                      f"Monthly profit: {format_currency(profit['monthly'])}."
        })
        
        # Category Performance
        if category.get('best_category'):
            sections.append({
                "title": "Category Performance",
                "content": f"Best performing category: {category['best_category']['name']} "
                          f"with {format_currency(category['best_category']['revenue'])} revenue. "
                          f"Worst category: {category['worst_category']['name']} "
                          f"with {format_currency(category['worst_category']['revenue'])} revenue."
            })
        
        # Inventory Health
        sections.append({
            "title": "Inventory Health",
            "content": f"Inventory value: {format_currency(inventory['inventory_value'])}. "
                      f"Stock health score: {inventory['stock_health']:.1f}%. "
                      f"{inventory['low_stock']} products are low on stock."
        })
        
        # Recommendations
        recommendations = []
        if growth['weekly_growth']['revenue'] < 0:
            recommendations.append("Revenue is declining - consider promotional campaigns")
        if health['score'] < 50:
            recommendations.append("Business health is critical - immediate action required")
        if inventory['low_stock'] > 10:
            recommendations.append(f"Stock levels are low for {inventory['low_stock']} products - restock soon")
        if category.get('worst_category') and category['worst_category'].get('revenue', 0) < 100:
            recommendations.append(f"Category '{category['worst_category']['name']}' needs attention")
        
        sections.append({
            "title": "Recommendations",
            "content": "\n".join(recommendations) if recommendations else "Business is performing well - maintain current strategy"
        })
        
        return {
            "report": sections,
            "generated_at": datetime.utcnow().isoformat(),
            "summary": health['status']
        }
    
    def generate_insights(self) -> List[Dict[str, Any]]:
        """
        Generate business insights.
        
        Returns:
            List[Dict]: Business insights
        """
        self._ensure_data_loaded()
        
        if self.sales_df.empty:
            return [{"type": "info", "message": "No data available for insights"}]
        
        insights = []
        
        # Get analytics
        revenue = self.get_revenue_analytics()
        profit = self.get_profit_analytics()
        growth = self.get_growth_analytics()
        health = self.get_business_health()
        inventory = self.get_inventory_analytics()
        category = self.get_category_analytics()
        kpis = self.get_kpis()
        
        # Revenue insights
        if growth['weekly_growth']['revenue'] > 10:
            insights.append({
                "type": "positive",
                "category": "revenue",
                "message": f"Revenue is growing strongly at {growth['weekly_growth']['revenue']:.1f}% this week",
                "priority": "high"
            })
        elif growth['weekly_growth']['revenue'] > 0:
            insights.append({
                "type": "neutral",
                "category": "revenue",
                "message": f"Revenue is stable with {growth['weekly_growth']['revenue']:.1f}% growth",
                "priority": "medium"
            })
        else:
            insights.append({
                "type": "negative",
                "category": "revenue",
                "message": f"Revenue is declining by {abs(growth['weekly_growth']['revenue']):.1f}% - needs attention",
                "priority": "high"
            })
        
        # Profit insights
        if health['details']['profit_margin'] > 20:
            insights.append({
                "type": "positive",
                "category": "profit",
                "message": f"Profit margin is healthy at {health['details']['profit_margin']:.1f}%",
                "priority": "medium"
            })
        elif health['details']['profit_margin'] < 10:
            insights.append({
                "type": "negative",
                "category": "profit",
                "message": f"Profit margin is low at {health['details']['profit_margin']:.1f}% - needs improvement",
                "priority": "high"
            })
        
        # Inventory insights
        if inventory['low_stock'] > 5:
            insights.append({
                "type": "warning",
                "category": "inventory",
                "message": f"{inventory['low_stock']} products are low on stock - consider restocking",
                "priority": "high"
            })
        
        if inventory['out_of_stock'] > 0:
            insights.append({
                "type": "critical",
                "category": "inventory",
                "message": f"{inventory['out_of_stock']} products are out of stock - immediate action needed",
                "priority": "critical"
            })
        
        # Category insights
        if category.get('best_category'):
            insights.append({
                "type": "positive",
                "category": "category",
                "message": f"'{category['best_category']['name']}' is the best performing category",
                "priority": "low"
            })
        
        if category.get('worst_category') and category['worst_category'].get('revenue', 0) < 100:
            insights.append({
                "type": "warning",
                "category": "category",
                "message": f"'{category['worst_category']['name']}' is underperforming - needs attention",
                "priority": "medium"
            })
        
        # Overall health insight
        if health['score'] >= 80:
            insights.append({
                "type": "positive",
                "category": "overall",
                "message": "Business health is excellent - maintain current strategy",
                "priority": "low"
            })
        elif health['score'] >= 60:
            insights.append({
                "type": "neutral",
                "category": "overall",
                "message": "Business health is good - look for optimization opportunities",
                "priority": "low"
            })
        else:
            insights.append({
                "type": "critical",
                "category": "overall",
                "message": f"Business health is {health['status'].lower()} ({health['score']}/100) - immediate action required",
                "priority": "critical"
            })
        
        return insights
    
    def _calculate_inventory_health(self) -> float:
        """Calculate inventory health score."""
        if self.products_df.empty:
            return 0
        
        # Calculate various health metrics
        total_products = len(self.products_df)
        if total_products == 0:
            return 0
        
        out_of_stock_ratio = len(self.products_df[self.products_df['stock'] == 0]) / total_products
        low_stock_ratio = len(self.products_df[self.products_df['stock'] <= self.products_df['minimum_stock']]) / total_products
        
        # Calculate health score
        health_score = 100 - (out_of_stock_ratio * 50) - (low_stock_ratio * 30)
        return max(0, min(100, health_score))
    
    def _calculate_customer_health(self) -> float:
        """Calculate customer health score."""
        if self.sales_df.empty:
            return 0
        
        # Check for repeat customers
        if 'customer_name' not in self.sales_df.columns:
            return 50  # Default if no customer data
        
        customer_counts = self.sales_df['customer_name'].value_counts()
        repeat_customers = len(customer_counts[customer_counts > 1])
        total_customers = len(customer_counts)
        
        if total_customers == 0:
            return 0
        
        repeat_ratio = repeat_customers / total_customers
        return 50 + (repeat_ratio * 50)
    
    def _calculate_low_stock_ratio(self) -> float:
        """Calculate low stock ratio."""
        if self.products_df.empty:
            return 0
        
        total = len(self.products_df)
        if total == 0:
            return 0
        
        low_stock = len(self.products_df[self.products_df['stock'] <= self.products_df['minimum_stock']])
        return low_stock / total
    
    def _empty_analytics(self, category: str) -> Dict[str, Any]:
        """Return empty analytics data."""
        return {
            "message": f"No data available for {category} analytics",
            "data": {}
        }


# Create singleton instance
analytics_engine = AnalyticsEngine()