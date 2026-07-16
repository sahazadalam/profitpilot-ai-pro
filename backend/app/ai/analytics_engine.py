"""
Analytics Engine for business intelligence.
Uses pandas and numpy for data analysis.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
import logging
import traceback

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
            self.sales_df = pd.DataFrame(sales_data) if sales_data else pd.DataFrame()
            self.products_df = pd.DataFrame(products_data) if products_data else pd.DataFrame()
            
            # Clean and prepare data
            if not self.sales_df.empty:
                if 'sale_date' in self.sales_df.columns:
                    self.sales_df['sale_date'] = pd.to_datetime(self.sales_df['sale_date'])
                if 'total_sale_amount' in self.sales_df.columns:
                    self.sales_df['total_sale_amount'] = pd.to_numeric(self.sales_df['total_sale_amount'], errors='coerce')
                if 'profit' in self.sales_df.columns:
                    self.sales_df['profit'] = pd.to_numeric(self.sales_df['profit'], errors='coerce')
                if 'quantity' in self.sales_df.columns:
                    self.sales_df['quantity'] = pd.to_numeric(self.sales_df['quantity'], errors='coerce')
                
                # Fill NaN values
                self.sales_df = self.sales_df.fillna(0)
            
            if not self.products_df.empty:
                if 'stock' in self.products_df.columns:
                    self.products_df['stock'] = pd.to_numeric(self.products_df['stock'], errors='coerce')
                if 'purchase_price' in self.products_df.columns:
                    self.products_df['purchase_price'] = pd.to_numeric(self.products_df['purchase_price'], errors='coerce')
                if 'minimum_stock' in self.products_df.columns:
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
        try:
            self._ensure_data_loaded()
            
            if self.sales_df.empty or 'total_sale_amount' not in self.sales_df.columns:
                return {
                    "today": 0,
                    "weekly": 0,
                    "monthly": 0,
                    "yearly": 0,
                    "total": 0
                }
            
            now = datetime.utcnow()
            
            # Calculate periods
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            week_start = today_start - timedelta(days=7)
            month_start = today_start - timedelta(days=30)
            year_start = today_start - timedelta(days=365)
            
            # Filter by periods
            if 'sale_date' in self.sales_df.columns:
                today_sales = self.sales_df[self.sales_df['sale_date'] >= today_start]
                week_sales = self.sales_df[self.sales_df['sale_date'] >= week_start]
                month_sales = self.sales_df[self.sales_df['sale_date'] >= month_start]
                year_sales = self.sales_df[self.sales_df['sale_date'] >= year_start]
            else:
                today_sales = self.sales_df
                week_sales = self.sales_df
                month_sales = self.sales_df
                year_sales = self.sales_df
            
            total_revenue = self.sales_df['total_sale_amount'].sum()
            
            return {
                "today": float(today_sales['total_sale_amount'].sum()) if not today_sales.empty else 0,
                "weekly": float(week_sales['total_sale_amount'].sum()) if not week_sales.empty else 0,
                "monthly": float(month_sales['total_sale_amount'].sum()) if not month_sales.empty else 0,
                "yearly": float(year_sales['total_sale_amount'].sum()) if not year_sales.empty else 0,
                "total": float(total_revenue)
            }
        except Exception as e:
            logger.error(f"Error in get_revenue_analytics: {str(e)}")
            return {"today": 0, "weekly": 0, "monthly": 0, "yearly": 0, "total": 0}
    
    def get_profit_analytics(self) -> Dict[str, Any]:
        """
        Calculate profit analytics.
        
        Returns:
            Dict: Profit analytics data
        """
        try:
            self._ensure_data_loaded()
            
            if self.sales_df.empty or 'profit' not in self.sales_df.columns:
                return {
                    "today": 0,
                    "weekly": 0,
                    "monthly": 0,
                    "yearly": 0,
                    "total": 0
                }
            
            now = datetime.utcnow()
            
            # Calculate periods
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            week_start = today_start - timedelta(days=7)
            month_start = today_start - timedelta(days=30)
            year_start = today_start - timedelta(days=365)
            
            # Filter by periods
            if 'sale_date' in self.sales_df.columns:
                today_sales = self.sales_df[self.sales_df['sale_date'] >= today_start]
                week_sales = self.sales_df[self.sales_df['sale_date'] >= week_start]
                month_sales = self.sales_df[self.sales_df['sale_date'] >= month_start]
                year_sales = self.sales_df[self.sales_df['sale_date'] >= year_start]
            else:
                today_sales = self.sales_df
                week_sales = self.sales_df
                month_sales = self.sales_df
                year_sales = self.sales_df
            
            return {
                "today": float(today_sales['profit'].sum()) if not today_sales.empty else 0,
                "weekly": float(week_sales['profit'].sum()) if not week_sales.empty else 0,
                "monthly": float(month_sales['profit'].sum()) if not month_sales.empty else 0,
                "yearly": float(year_sales['profit'].sum()) if not year_sales.empty else 0,
                "total": float(self.sales_df['profit'].sum())
            }
        except Exception as e:
            logger.error(f"Error in get_profit_analytics: {str(e)}")
            return {"today": 0, "weekly": 0, "monthly": 0, "yearly": 0, "total": 0}
    
    def get_business_health(self) -> Dict[str, Any]:
        """
        Calculate business health score.
        
        Returns:
            Dict: Business health data
        """
        try:
            self._ensure_data_loaded()
            
            if self.sales_df.empty:
                return {
                    "score": 50,
                    "status": "Average",
                    "explanation": "No sales data available for health calculation.",
                    "details": {
                        "revenue_growth": 0,
                        "profit_margin": 0,
                        "inventory_health": 50,
                        "sales_trend": "unknown",
                        "low_stock_ratio": 0
                    }
                }
            
            # Calculate metrics
            revenue_analytics = self.get_revenue_analytics()
            profit_analytics = self.get_profit_analytics()
            
            total_revenue = revenue_analytics.get('total', 0)
            total_profit = profit_analytics.get('total', 0)
            
            # Calculate profit margin
            profit_margin = 0
            if total_revenue != 0:
                profit_margin = (total_profit / total_revenue) * 100
            
            # Calculate inventory health
            inventory_health = self._calculate_inventory_health()
            
            # Calculate customer health
            customer_health = self._calculate_customer_health()
            
            # Calculate growth
            weekly_growth = self._calculate_weekly_growth()
            
            # Calculate score
            score = self._calculate_health_score(
                revenue_growth=weekly_growth,
                profit_margin=profit_margin,
                inventory_health=inventory_health,
                customer_health=customer_health
            )
            
            status = self._get_status(score)
            explanation = self._generate_explanation(score, weekly_growth, profit_margin, inventory_health)
            
            return {
                "score": score,
                "status": status,
                "explanation": explanation,
                "details": {
                    "revenue_growth": round(weekly_growth, 2),
                    "profit_margin": round(profit_margin, 2),
                    "inventory_health": round(inventory_health, 2),
                    "sales_trend": "upward" if weekly_growth > 0 else "downward" if weekly_growth < 0 else "stable",
                    "low_stock_ratio": self._calculate_low_stock_ratio()
                }
            }
        except Exception as e:
            logger.error(f"Error in get_business_health: {str(e)}\n{traceback.format_exc()}")
            return {
                "score": 50,
                "status": "Average",
                "explanation": f"Error calculating health: {str(e)}",
                "details": {
                    "revenue_growth": 0,
                    "profit_margin": 0,
                    "inventory_health": 50,
                    "sales_trend": "unknown",
                    "low_stock_ratio": 0
                }
            }
    
    def _calculate_weekly_growth(self) -> float:
        """Calculate weekly revenue growth."""
        try:
            if self.sales_df.empty or 'sale_date' not in self.sales_df.columns:
                return 0
            
            # Group by date
            daily_revenue = self.sales_df.groupby(self.sales_df['sale_date'].dt.date)['total_sale_amount'].sum()
            
            if len(daily_revenue) < 2:
                return 0
            
            current_week = daily_revenue.tail(7).sum()
            previous_week = daily_revenue.iloc[-14:-7].sum() if len(daily_revenue) >= 14 else current_week
            
            if previous_week == 0:
                return 0 if current_week == 0 else 100
            
            return ((current_week - previous_week) / abs(previous_week)) * 100
        except Exception as e:
            logger.error(f"Error calculating weekly growth: {str(e)}")
            return 0
    
    def _calculate_health_score(self, revenue_growth: float, profit_margin: float, 
                                inventory_health: float, customer_health: float) -> int:
        """Calculate overall health score."""
        try:
            scores = []
            
            # Revenue growth score (0-25)
            if revenue_growth >= 20:
                scores.append(25)
            elif revenue_growth >= 10:
                scores.append(20)
            elif revenue_growth >= 5:
                scores.append(15)
            elif revenue_growth >= 0:
                scores.append(10)
            else:
                scores.append(5)
            
            # Profit margin score (0-25)
            if profit_margin >= 30:
                scores.append(25)
            elif profit_margin >= 20:
                scores.append(20)
            elif profit_margin >= 10:
                scores.append(15)
            elif profit_margin >= 5:
                scores.append(10)
            else:
                scores.append(5)
            
            # Inventory health score (0-25)
            scores.append(min(25, inventory_health * 0.25))
            
            # Customer health score (0-25)
            scores.append(min(25, customer_health * 0.25))
            
            return int(sum(scores))
        except Exception as e:
            logger.error(f"Error calculating health score: {str(e)}")
            return 50
    
    def _get_status(self, score: int) -> str:
        """Get status based on score."""
        if score >= 80:
            return "Excellent"
        elif score >= 65:
            return "Good"
        elif score >= 50:
            return "Average"
        elif score >= 35:
            return "Poor"
        else:
            return "Critical"
    
    def _generate_explanation(self, score: int, revenue_growth: float, 
                              profit_margin: float, inventory_health: float) -> str:
        """Generate explanation for health score."""
        status = self._get_status(score)
        
        explanation = f"Business Health Score: {score}/100 - {status}\n\n"
        explanation += f"Revenue Growth: {revenue_growth:.1f}%\n"
        explanation += f"Profit Margin: {profit_margin:.1f}%\n"
        explanation += f"Inventory Health: {inventory_health:.1f}%\n\n"
        
        # Add recommendations
        if revenue_growth < 0:
            explanation += "⚠️ Revenue is declining - consider promotional campaigns\n"
        if profit_margin < 10:
            explanation += "⚠️ Profit margin is low - review pricing and costs\n"
        if inventory_health < 50:
            explanation += "⚠️ Inventory health needs improvement - review stock levels\n"
        if score >= 65:
            explanation += "✅ Business is performing well - maintain current strategy"
        else:
            explanation += "📈 Focus on improving key metrics to boost health score"
        
        return explanation
    
    def _calculate_inventory_health(self) -> float:
        """Calculate inventory health score."""
        try:
            if self.products_df.empty:
                return 50
            
            total_products = len(self.products_df)
            if total_products == 0:
                return 50
            
            if 'stock' not in self.products_df.columns or 'minimum_stock' not in self.products_df.columns:
                return 50
            
            low_stock = len(self.products_df[self.products_df['stock'] <= self.products_df['minimum_stock']])
            out_of_stock = len(self.products_df[self.products_df['stock'] == 0])
            
            health_score = 100 - (out_of_stock / total_products * 50) - (low_stock / total_products * 30)
            return max(0, min(100, health_score))
        except Exception as e:
            logger.error(f"Error calculating inventory health: {str(e)}")
            return 50
    
    def _calculate_customer_health(self) -> float:
        """Calculate customer health score."""
        try:
            if self.sales_df.empty or 'customer_name' not in self.sales_df.columns:
                return 50
            
            customer_counts = self.sales_df['customer_name'].value_counts()
            total_customers = len(customer_counts)
            
            if total_customers == 0:
                return 50
            
            repeat_customers = len(customer_counts[customer_counts > 1])
            repeat_ratio = repeat_customers / total_customers
            
            return 50 + (repeat_ratio * 50)
        except Exception as e:
            logger.error(f"Error calculating customer health: {str(e)}")
            return 50
    
    def _calculate_low_stock_ratio(self) -> float:
        """Calculate low stock ratio."""
        try:
            if self.products_df.empty:
                return 0
            
            total = len(self.products_df)
            if total == 0:
                return 0
            
            if 'stock' in self.products_df.columns and 'minimum_stock' in self.products_df.columns:
                low_stock = len(self.products_df[self.products_df['stock'] <= self.products_df['minimum_stock']])
                return low_stock / total
            
            return 0
        except Exception as e:
            logger.error(f"Error calculating low stock ratio: {str(e)}")
            return 0
    
    def get_top_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top selling products."""
        try:
            self._ensure_data_loaded()
            
            if self.sales_df.empty or 'product_id' not in self.sales_df.columns:
                return []
            
            # Group by product
            product_sales = self.sales_df.groupby('product_id').agg({
                'product_name': 'first' if 'product_name' in self.sales_df.columns else lambda x: '',
                'category': 'first' if 'category' in self.sales_df.columns else lambda x: '',
                'quantity': 'sum' if 'quantity' in self.sales_df.columns else lambda x: 0,
                'total_sale_amount': 'sum' if 'total_sale_amount' in self.sales_df.columns else lambda x: 0,
                'profit': 'sum' if 'profit' in self.sales_df.columns else lambda x: 0
            }).reset_index()
            
            # Sort by quantity sold
            if 'quantity' in product_sales.columns:
                top_products = product_sales.sort_values('quantity', ascending=False).head(limit)
            else:
                top_products = product_sales.head(limit)
            
            return top_products.to_dict('records')
        except Exception as e:
            logger.error(f"Error in get_top_products: {str(e)}")
            return []
    
    def get_worst_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get worst selling products."""
        try:
            self._ensure_data_loaded()
            
            if self.sales_df.empty or 'product_id' not in self.sales_df.columns:
                return []
            
            product_sales = self.sales_df.groupby('product_id').agg({
                'product_name': 'first' if 'product_name' in self.sales_df.columns else lambda x: '',
                'category': 'first' if 'category' in self.sales_df.columns else lambda x: '',
                'quantity': 'sum' if 'quantity' in self.sales_df.columns else lambda x: 0,
                'total_sale_amount': 'sum' if 'total_sale_amount' in self.sales_df.columns else lambda x: 0,
                'profit': 'sum' if 'profit' in self.sales_df.columns else lambda x: 0
            }).reset_index()
            
            if 'quantity' in product_sales.columns:
                worst_products = product_sales.sort_values('quantity', ascending=True).head(limit)
            else:
                worst_products = product_sales.head(limit)
            
            return worst_products.to_dict('records')
        except Exception as e:
            logger.error(f"Error in get_worst_products: {str(e)}")
            return []
    
    def get_category_analytics(self) -> Dict[str, Any]:
        """Get category analytics."""
        try:
            self._ensure_data_loaded()
            
            if self.sales_df.empty or 'category' not in self.sales_df.columns:
                return {
                    "data": [],
                    "best_category": {"name": None, "revenue": 0, "profit": 0},
                    "worst_category": {"name": None, "revenue": 0, "profit": 0}
                }
            
            # Group by category
            category_analytics = self.sales_df.groupby('category').agg({
                'total_sale_amount': 'sum' if 'total_sale_amount' in self.sales_df.columns else lambda x: 0,
                'profit': 'sum' if 'profit' in self.sales_df.columns else lambda x: 0,
                'quantity': 'sum' if 'quantity' in self.sales_df.columns else lambda x: 0
            }).reset_index()
            
            # Sort by revenue
            if 'total_sale_amount' in category_analytics.columns:
                category_analytics = category_analytics.sort_values('total_sale_amount', ascending=False)
            
            best_category = category_analytics.iloc[0] if not category_analytics.empty else None
            worst_category = category_analytics.iloc[-1] if not category_analytics.empty else None
            
            return {
                "data": category_analytics.to_dict('records'),
                "best_category": {
                    "name": best_category['category'] if best_category is not None else None,
                    "revenue": float(best_category['total_sale_amount']) if best_category is not None else 0,
                    "profit": float(best_category['profit']) if best_category is not None else 0
                } if best_category is not None else {"name": None, "revenue": 0, "profit": 0},
                "worst_category": {
                    "name": worst_category['category'] if worst_category is not None else None,
                    "revenue": float(worst_category['total_sale_amount']) if worst_category is not None else 0,
                    "profit": float(worst_category['profit']) if worst_category is not None else 0
                } if worst_category is not None else {"name": None, "revenue": 0, "profit": 0}
            }
        except Exception as e:
            logger.error(f"Error in get_category_analytics: {str(e)}")
            return {"data": [], "best_category": {}, "worst_category": {}}
    
    def get_inventory_analytics(self) -> Dict[str, Any]:
        """Get inventory analytics."""
        try:
            self._ensure_data_loaded()
            
            if self.products_df.empty:
                return {
                    "total_products": 0,
                    "total_stock": 0,
                    "inventory_value": 0,
                    "out_of_stock": 0,
                    "low_stock": 0,
                    "average_stock": 0,
                    "stock_health": 50
                }
            
            total_products = len(self.products_df)
            total_stock = self.products_df['stock'].sum() if 'stock' in self.products_df.columns else 0
            inventory_value = (self.products_df['stock'] * self.products_df['purchase_price']).sum() if 'stock' in self.products_df.columns and 'purchase_price' in self.products_df.columns else 0
            out_of_stock = len(self.products_df[self.products_df['stock'] == 0]) if 'stock' in self.products_df.columns else 0
            low_stock = len(self.products_df[self.products_df['stock'] <= self.products_df['minimum_stock']]) if 'stock' in self.products_df.columns and 'minimum_stock' in self.products_df.columns else 0
            avg_stock = self.products_df['stock'].mean() if 'stock' in self.products_df.columns else 0
            
            return {
                "total_products": total_products,
                "total_stock": int(total_stock),
                "inventory_value": float(inventory_value),
                "out_of_stock": out_of_stock,
                "low_stock": low_stock,
                "average_stock": float(avg_stock),
                "stock_health": self._calculate_inventory_health()
            }
        except Exception as e:
            logger.error(f"Error in get_inventory_analytics: {str(e)}")
            return {"total_products": 0, "total_stock": 0, "inventory_value": 0, "out_of_stock": 0, "low_stock": 0, "average_stock": 0, "stock_health": 50}
    
    def get_kpis(self) -> Dict[str, Any]:
        """Get key performance indicators."""
        try:
            self._ensure_data_loaded()
            
            if self.sales_df.empty:
                return {
                    "revenue": 0,
                    "profit": 0,
                    "sales": 0,
                    "orders": 0,
                    "products": 0,
                    "average_order_value": 0,
                    "average_profit_per_sale": 0
                }
            
            total_revenue = self.sales_df['total_sale_amount'].sum() if 'total_sale_amount' in self.sales_df.columns else 0
            total_profit = self.sales_df['profit'].sum() if 'profit' in self.sales_df.columns else 0
            total_sales = len(self.sales_df)
            total_orders = self.sales_df['invoice_number'].nunique() if 'invoice_number' in self.sales_df.columns else total_sales
            total_products = len(self.products_df) if not self.products_df.empty else 0
            
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
        except Exception as e:
            logger.error(f"Error in get_kpis: {str(e)}")
            return {"revenue": 0, "profit": 0, "sales": 0, "orders": 0, "products": 0, "average_order_value": 0, "average_profit_per_sale": 0}
    
    def get_trends(self) -> Dict[str, Any]:
        """Get trend analytics."""
        try:
            self._ensure_data_loaded()
            
            if self.sales_df.empty or 'sale_date' not in self.sales_df.columns:
                return {
                    "daily": {"dates": [], "revenue": [], "profit": []},
                    "weekly": {"periods": [], "revenue": [], "profit": []},
                    "monthly": {"periods": [], "revenue": [], "profit": []}
                }
            
            # Daily trend (last 30 days)
            daily_trend = self.sales_df.groupby(self.sales_df['sale_date'].dt.date).agg({
                'total_sale_amount': 'sum' if 'total_sale_amount' in self.sales_df.columns else lambda x: 0,
                'profit': 'sum' if 'profit' in self.sales_df.columns else lambda x: 0
            }).reset_index().tail(30)
            
            return {
                "daily": {
                    "dates": daily_trend['sale_date'].astype(str).tolist() if not daily_trend.empty and 'sale_date' in daily_trend.columns else [],
                    "revenue": daily_trend['total_sale_amount'].tolist() if not daily_trend.empty and 'total_sale_amount' in daily_trend.columns else [],
                    "profit": daily_trend['profit'].tolist() if not daily_trend.empty and 'profit' in daily_trend.columns else []
                },
                "weekly": {
                    "periods": [],
                    "revenue": [],
                    "profit": []
                },
                "monthly": {
                    "periods": [],
                    "revenue": [],
                    "profit": []
                }
            }
        except Exception as e:
            logger.error(f"Error in get_trends: {str(e)}")
            return {"daily": {"dates": [], "revenue": [], "profit": []}, "weekly": {"periods": [], "revenue": [], "profit": []}, "monthly": {"periods": [], "revenue": [], "profit": []}}
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate AI-style business report."""
        try:
            self._ensure_data_loaded()
            
            if self.sales_df.empty:
                return {
                    "report": [{
                        "title": "No Data Available",
                        "content": "No sales data found. Start recording sales to generate reports."
                    }],
                    "generated_at": datetime.utcnow().isoformat(),
                    "summary": "No Data"
                }
            
            revenue = self.get_revenue_analytics()
            profit = self.get_profit_analytics()
            health = self.get_business_health()
            
            sections = []
            
            # Executive Summary
            sections.append({
                "title": "Executive Summary",
                "content": f"Business is performing with a health score of {health.get('score', 0)}/100 ({health.get('status', 'Unknown')}). " +
                          f"Total revenue: ${revenue.get('total', 0):,.2f} with ${profit.get('total', 0):,.2f} profit."
            })
            
            # Revenue Analysis
            sections.append({
                "title": "Revenue Analysis",
                "content": f"Monthly revenue: ${revenue.get('monthly', 0):,.2f}. " +
                          f"Today's revenue: ${revenue.get('today', 0):,.2f}."
            })
            
            # Profit Analysis
            sections.append({
                "title": "Profit Analysis",
                "content": f"Profit margin is {health.get('details', {}).get('profit_margin', 0):.1f}%. " +
                          f"Monthly profit: ${profit.get('monthly', 0):,.2f}."
            })
            
            # Recommendations
            recommendations = []
            if health.get('score', 0) < 50:
                recommendations.append("Business health is critical - immediate action required")
            if len(recommendations) == 0:
                recommendations.append("Business is performing well - maintain current strategy")
            
            sections.append({
                "title": "Recommendations",
                "content": "\n".join(recommendations)
            })
            
            return {
                "report": sections,
                "generated_at": datetime.utcnow().isoformat(),
                "summary": health.get('status', 'Unknown')
            }
        except Exception as e:
            logger.error(f"Error in generate_report: {str(e)}\n{traceback.format_exc()}")
            return {
                "report": [{"title": "Error", "content": f"Error generating report: {str(e)}"}],
                "generated_at": datetime.utcnow().isoformat(),
                "summary": "Error"
            }
    
    def generate_insights(self) -> List[Dict[str, Any]]:
        """Generate business insights."""
        try:
            self._ensure_data_loaded()
            
            if self.sales_df.empty:
                return [{
                    "type": "info",
                    "category": "general",
                    "message": "No sales data available. Start making sales to get insights.",
                    "priority": "low"
                }]
            
            insights = []
            health = self.get_business_health()
            inventory = self.get_inventory_analytics()
            
            # Inventory insights
            if inventory.get('low_stock', 0) > 5:
                insights.append({
                    "type": "warning",
                    "category": "inventory",
                    "message": f"{inventory['low_stock']} products are low on stock - consider restocking",
                    "priority": "high"
                })
            
            if inventory.get('out_of_stock', 0) > 0:
                insights.append({
                    "type": "critical",
                    "category": "inventory",
                    "message": f"{inventory['out_of_stock']} products are out of stock - immediate action needed",
                    "priority": "critical"
                })
            
            # Overall health insight
            health_score = health.get('score', 0)
            if health_score >= 80:
                insights.append({
                    "type": "positive",
                    "category": "overall",
                    "message": "Business health is excellent - maintain current strategy",
                    "priority": "low"
                })
            elif health_score >= 60:
                insights.append({
                    "type": "neutral",
                    "category": "overall",
                    "message": "Business health is good - look for optimization opportunities",
                    "priority": "low"
                })
            else:
                status = health.get('status', 'unknown')
                insights.append({
                    "type": "critical",
                    "category": "overall",
                    "message": f"Business health is {status.lower()} ({health_score}/100) - review recommended",
                    "priority": "critical"
                })
            
            return insights
        except Exception as e:
            logger.error(f"Error in generate_insights: {str(e)}\n{traceback.format_exc()}")
            return [{
                "type": "info",
                "category": "general",
                "message": f"Error generating insights: {str(e)}",
                "priority": "low"
            }]
    
    def get_growth_analytics(self) -> Dict[str, Any]:
        """Get growth analytics."""
        try:
            self._ensure_data_loaded()
            
            if self.sales_df.empty:
                return {
                    "daily": {"revenue": 0, "profit": 0},
                    "weekly_growth": {"revenue": 0, "profit": 0},
                    "monthly_growth": {"revenue": 0, "profit": 0},
                    "moving_averages": {"revenue_7d": 0, "profit_7d": 0}
                }
            
            weekly_growth = self._calculate_weekly_growth()
            
            return {
                "daily": {
                    "revenue": float(self.sales_df['total_sale_amount'].iloc[-1]) if not self.sales_df.empty and 'total_sale_amount' in self.sales_df.columns else 0,
                    "profit": float(self.sales_df['profit'].iloc[-1]) if not self.sales_df.empty and 'profit' in self.sales_df.columns else 0
                },
                "weekly_growth": {
                    "revenue": weekly_growth,
                    "profit": 0
                },
                "monthly_growth": {
                    "revenue": 0,
                    "profit": 0
                },
                "moving_averages": {
                    "revenue_7d": 0,
                    "profit_7d": 0
                }
            }
        except Exception as e:
            logger.error(f"Error in get_growth_analytics: {str(e)}")
            return {"daily": {"revenue": 0, "profit": 0}, "weekly_growth": {"revenue": 0, "profit": 0}, "monthly_growth": {"revenue": 0, "profit": 0}, "moving_averages": {"revenue_7d": 0, "profit_7d": 0}}


# Create singleton instance
analytics_engine = AnalyticsEngine()