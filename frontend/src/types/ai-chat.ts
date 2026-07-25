export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  metadata?: {
    confidence?: number;
    query_type?: string;
    sources?: string[];
  };
}

export interface ChatRequest {
  question: string;
  conversation_id?: string;
}

export interface ChatResponse {
  answer: string;
  confidence: number;
  reasoning: string;
  recommendations: string[];
  sources: string[];
  conversation_id: string;
  query_type: string;
  timestamp: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  conversation_id: string;
  messages: ChatMessage[];
  created_at: string;
  updated_at: string;
  summary?: string;
}

export interface ChatHistory {
  messages: ChatMessage[];
  conversation_id: string;
}

export interface SuggestedQuestion {
  id: string;
  question: string;
  category: string;
  icon: string;
}

export interface Report {
  period: string;
  generated_at: string;
  start_date?: string;
  end_date?: string;
  summary?: string;
  report?: string;
  error?: string;
}

export interface ExecutiveSummary {
  period: string;
  generated_at: string;
  total_recommendations: number;
  high_priority: number;
  restock_needed: number;
  pricing_suggestions: number;
  loss_products: number;
  business_risk: string;
  risk_score: number;
  total_products: number;
  total_sales: number;
  total_revenue: number;
  total_profit: number;
  profit_margin: number;
  top_products: any[];
  summary: string;
}

export interface BusinessAlert {
  type: 'critical' | 'high' | 'medium' | 'low';
  message: string;
  action: string;
  category: string;
}

export interface ActionPlan {
  actions: {
    critical: Array<{
      action: string;
      details: string;
      expected_benefit: string;
      estimated_impact: string;
    }>;
    high: Array<{
      action: string;
      details: string;
      expected_benefit: string;
      estimated_impact: string;
    }>;
    medium: Array<{
      action: string;
      details: string;
      expected_benefit: string;
      estimated_impact: string;
    }>;
    low: Array<{
      action: string;
      details: string;
      expected_benefit: string;
      estimated_impact: string;
    }>;
  };
  generated_at: string;
  total_actions: number;
}
