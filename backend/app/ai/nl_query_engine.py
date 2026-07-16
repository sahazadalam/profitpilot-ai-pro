"""
Natural Language Query Engine for understanding user questions.
"""
import re
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class NLQueryEngine:
    """
    Natural Language Query Engine for understanding business questions.
    """
    
    def __init__(self):
        """Initialize the NL query engine."""
        self.keywords = {
            "inventory": ["stock", "inventory", "restock", "low stock", "out of stock", "supply"],
            "sales": ["sale", "sales", "revenue", "profit", "selling", "customers", "orders"],
            "analytics": ["analytics", "insights", "trends", "patterns", "performance"],
            "forecasting": ["forecast", "predict", "future", "next", "upcoming", "demand"],
            "recommendation": ["recommend", "suggestion", "advice", "should", "better", "best"],
            "risk": ["risk", "danger", "threat", "warning", "caution"],
            "health": ["health", "healthy", "score", "rating"],
            "report": ["report", "summary", "overview", "status"]
        }
        
        self.question_patterns = {
            "best_product": r"(best|top|highest).*(product|selling|revenue)",
            "worst_product": r"(worst|lowest|poorest).*(product|selling|revenue)",
            "revenue": r"revenue|income|sales amount",
            "profit": r"profit|margin|earnings",
            "growth": r"growth|increase|decrease|trend",
            "forecast": r"forecast|predict|future|will|next",
            "restock": r"restock|reorder|replenish|order",
            "loss": r"loss|losses|unprofitable",
            "health": r"health|healthy|score|rating",
            "risk": r"risk|danger|threat|warning",
            "customers": r"customer|buyer|client|user",
            "kpis": r"kpi|metric|performance|indicator",
            "category": r"category|department|section|division"
        }
    
    def classify_query(self, question: str) -> Tuple[str, Dict[str, Any]]:
        """
        Classify user question and extract intent.
        
        Args:
            question: User question
            
        Returns:
            Tuple[str, Dict[str, Any]]: Query type and extracted parameters
        """
        question_lower = question.lower()
        
        # Determine query type
        query_type = self._detect_query_type(question_lower)
        
        # Extract parameters
        params = self._extract_parameters(question_lower, query_type)
        
        # Detect specific intent
        intent = self._detect_intent(question_lower)
        
        return query_type, {
            "intent": intent,
            "params": params,
            "original_question": question
        }
    
    def _detect_query_type(self, question: str) -> str:
        """Detect the type of query."""
        # Check for each keyword category
        scores = {}
        
        for query_type, keywords in self.keywords.items():
            score = sum(1 for keyword in keywords if keyword in question)
            if score > 0:
                scores[query_type] = score
        
        if not scores:
            return "general"
        
        # Return the highest scoring type
        return max(scores, key=scores.get)
    
    def _detect_intent(self, question: str) -> str:
        """Detect specific intent from question."""
        for intent, pattern in self.question_patterns.items():
            if re.search(pattern, question, re.IGNORECASE):
                return intent
        
        return "general_query"
    
    def _extract_parameters(self, question: str, query_type: str) -> Dict[str, Any]:
        """Extract parameters from question."""
        params = {}
        
        # Extract time periods
        time_periods = {
            "today": ["today", "current", "now"],
            "yesterday": ["yesterday", "last day"],
            "this week": ["this week", "current week"],
            "last week": ["last week", "previous week"],
            "this month": ["this month", "current month"],
            "last month": ["last month", "previous month"],
            "this quarter": ["this quarter", "current quarter"],
            "last quarter": ["last quarter", "previous quarter"],
            "this year": ["this year", "current year"],
            "last year": ["last year", "previous year"]
        }
        
        for period, keywords in time_periods.items():
            if any(keyword in question for keyword in keywords):
                params["period"] = period
                break
        
        # Extract metrics
        if "revenue" in question:
            params["metric"] = "revenue"
        elif "profit" in question:
            params["metric"] = "profit"
        elif "sales" in question:
            params["metric"] = "sales"
        elif "growth" in question:
            params["metric"] = "growth"
        
        # Extract entities
        product_match = re.search(r"(product|item|sku)\s*['\"]?([^'\"]+)['\"]?", question)
        if product_match:
            params["product_name"] = product_match.group(2).strip()
        
        category_match = re.search(r"category\s*['\"]?([^'\"]+)['\"]?", question)
        if category_match:
            params["category"] = category_match.group(1).strip()
        
        return params


# Create singleton instance
nl_query_engine = NLQueryEngine()