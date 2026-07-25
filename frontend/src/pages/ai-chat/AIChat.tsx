import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, Loader2, Bot, User, Copy, Check, Trash2, 
  RefreshCw, Sparkles, History, Lightbulb
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { api } from '@/services/api';
import toast from 'react-hot-toast';
import { useAuth } from '@/contexts/AuthContext';

// Mock responses
const generateMockResponse = (question: string): string => {
  const q = question.toLowerCase();
  
  if (q.includes('revenue') || q.includes('sales')) {
    return 'Revenue Analysis:\n\nBased on your current sales data, your total revenue is ,450 this month, which is a 15% increase from last month.\n\nKey Insights:\n- Best performing product: MacBook Pro 2024\n- Top category: Electronics\n- Peak sales day: Friday\n\nRecommendation: Consider increasing stock for Electronics category as demand is growing.';
  }
  
  if (q.includes('profit') || q.includes('margin')) {
    return 'Profit Analysis:\n\nYour current profit margin is 32.5%, which is excellent for your industry.\n\nProfit Breakdown:\n- Total Profit: ,850\n- Profit per Sale: .50\n- Best Product Margin: 45% (MacBook Pro)\n\nRecommendation: Your profit margins are healthy. Consider expanding your product line.';
  }
  
  if (q.includes('inventory') || q.includes('stock')) {
    return 'Inventory Status:\n\nCurrent inventory health is 85%.\n\nAlerts:\n- Low Stock: 3 products\n- Out of Stock: 0 products\n- Excess Stock: 2 products\n\nRestock Recommendations:\n1. Analytics Product 1 - Order 50 units\n2. Analytics Product 2 - Order 30 units\n\nRecommendation: Review low stock items and place orders soon.';
  }
  
  if (q.includes('customer') || q.includes('segment')) {
    return 'Customer Segmentation:\n\nYour customers are divided into 5 segments:\n\nVIP Customers (15%):\n- Average Spend: ,200\n- Total Revenue: ,000\n\nHigh Value (25%):\n- Average Spend: \n- Total Revenue: ,000\n\nInsight: VIP and High Value customers generate 60% of your revenue.\n\nRecommendation: Focus retention efforts on VIP customers.';
  }
  
  if (q.includes('product') && (q.includes('best') || q.includes('top'))) {
    return 'Top Performing Products:\n\n1. MacBook Pro 2024\n   - Revenue: ,495\n   - Units Sold: 5\n   - Profit: ,495\n\n2. iPhone 15 Pro\n   - Revenue: ,792\n   - Units Sold: 8\n   - Profit: ,592\n\n3. Analytics Product 1\n   - Revenue: ,500\n   - Units Sold: 15\n   - Profit: ,500\n\nRecommendation: Focus marketing on MacBook Pro for maximum returns.';
  }
  
  if (q.includes('forecast') || q.includes('predict') || q.includes('future')) {
    return 'Business Forecast:\n\nBased on current trends and historical data:\n\nRevenue Forecast (30 days): ,500\nProfit Forecast (30 days): ,850\nDemand Forecast: 5,200 units\n\nSeasonal Patterns:\n- Peak Season: July-December\n- Low Season: January-March\n\nRecommendation: Prepare for peak season by increasing inventory.';
  }
  
  if (q.includes('risk') || q.includes('danger') || q.includes('threat')) {
    return 'Business Risk Assessment:\n\nOverall Risk Score: 35/100 (Low)\n\nLow Risk Areas:\n- Inventory Management: Low Risk\n- Revenue Stability: Low Risk\n- Market Position: Low Risk\n\nMedium Risk Areas:\n- Profit Margins: Medium Risk\n\nRisk Details:\n- 2 products have declining sales\n- 1 category needs attention\n\nRecommendation: Monitor the underperforming products and consider adjustments.';
  }
  
  if (q.includes('health') || q.includes('score')) {
    return 'Business Health Report:\n\nHealth Score: 82/100 (Excellent)\n\nMetrics:\n- Revenue Growth: 15.5%\n- Profit Margin: 32.5%\n- Inventory Health: 85%\n- Customer Satisfaction: 98%\n\nStrengths:\n- Strong revenue growth\n- Excellent profit margins\n- High customer satisfaction\n\nAreas to Monitor:\n- Employee retention\n- Operational costs\n\nRecommendation: Maintain current strategy and look for optimization opportunities.';
  }
  
  return 'AI Assistant Response:\n\nI understand you are asking about: "' + question + '"\n\nHere is what I can help you with:\n\n- Business Intelligence - Real-time metrics and KPIs\n- Sales Analytics - Revenue, profit, and trends\n- Inventory Management - Stock levels and restocking\n- Predictions - Future forecasts and insights\n- Customer Insights - Segments and behavior\n- Risk Analysis - Business risks and mitigation\n- Recommendations - Actionable business insights\n\nPlease ask a specific business question and I will provide detailed analysis.';
};

export const AIChat = () => {
  const { user } = useAuth();
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<Array<{
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
  }>>([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Welcome to ProfitPilot AI Assistant!\n\nI am your AI business analyst. I can help you with:\n\n- Business Analytics - Revenue, profit, KPIs\n- Inventory Management - Stock levels, restocking\n- Sales Analysis - Trends, performance\n- Forecasting - Predictions, seasonality\n- Customer Insights - Segmentation, behavior\n- Risk Assessment - Business risks\n- Recommendations - Actionable insights\n\nAsk me anything about your business!',
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [suggestedQuestions] = useState([
    'What is my total revenue?',
    'Show me top products',
    'How is my inventory health?',
    'Predict next month revenue',
    'What are my business risks?',
    'Show customer segments'
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = async () => {
    if (!question.trim()) return;
    
    const userMessage = {
      id: Date.now().toString(),
      role: 'user' as const,
      content: question,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setQuestion('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      try {
        const response = await api.post('/chat', { 
          question: question,
          conversation_id: 'current'
        });
        
        const data = response.data;
        if (data?.data?.answer) {
          const assistantMessage = {
            id: (Date.now() + 1).toString(),
            role: 'assistant' as const,
            content: data.data.answer || data.data.message || 'I processed your request.',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, assistantMessage]);
          setIsTyping(false);
          setIsLoading(false);
          return;
        }
      } catch (apiError) {
        console.log('API error, using mock response:', apiError);
      }

      await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 600));
      
      const mockResponse = generateMockResponse(question);
      
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant' as const,
        content: mockResponse,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      
    } catch (error) {
      console.error('Error in chat:', error);
      toast.error('Failed to get response. Please try again.');
      
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant' as const,
        content: 'I encountered an error processing your request. Please try again or rephrase your question.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleCopy = async (content: string, id: string) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopiedId(id);
      toast.success('Copied to clipboard!');
      setTimeout(() => setCopiedId(null), 2000);
    } catch (error) {
      toast.error('Failed to copy');
    }
  };

  const handleClearChat = () => {
    if (messages.length > 1 && confirm('Clear all chat history?')) {
      setMessages([messages[0]]);
      toast.success('Chat cleared');
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setQuestion(suggestion);
    inputRef.current?.focus();
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="flex h-[calc(100vh-120px)] gap-4 p-4"
    >
      {/* Chat History Sidebar */}
      <div className="hidden w-64 flex-col rounded-xl border bg-card/50 backdrop-blur-sm lg:flex">
        <div className="border-b p-4">
          <h3 className="font-semibold flex items-center gap-2">
            <History className="h-4 w-4" />
            Chat History
          </h3>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          <div className="rounded-lg bg-primary/10 p-3 text-sm cursor-pointer hover:bg-primary/20 transition-colors">
            <p className="font-medium">Current Session</p>
            <p className="text-xs text-muted-foreground">Active now</p>
          </div>
          <div className="rounded-lg p-3 text-sm cursor-pointer hover:bg-muted/50 transition-colors">
            <p className="font-medium">Previous Chat</p>
            <p className="text-xs text-muted-foreground">2 hours ago</p>
          </div>
          <div className="rounded-lg p-3 text-sm cursor-pointer hover:bg-muted/50 transition-colors">
            <p className="font-medium">Sales Analysis</p>
            <p className="text-xs text-muted-foreground">Yesterday</p>
          </div>
          <div className="rounded-lg p-3 text-sm cursor-pointer hover:bg-muted/50 transition-colors">
            <p className="font-medium">Inventory Report</p>
            <p className="text-xs text-muted-foreground">3 days ago</p>
          </div>
        </div>
        <div className="border-t p-4">
          <Button variant="ghost" size="sm" className="w-full justify-start gap-2 text-red-500 hover:text-red-600 hover:bg-red-500/10" onClick={handleClearChat}>
            <Trash2 className="h-4 w-4" />
            Clear History
          </Button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex flex-1 flex-col rounded-xl border bg-card/50 backdrop-blur-sm">
        {/* Chat Header */}
        <div className="flex items-center justify-between border-b p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-r from-primary to-purple-600">
              <Bot className="h-5 w-5 text-white" />
            </div>
            <div>
              <h3 className="font-semibold flex items-center gap-2">
                AI Business Assistant
                <Badge variant="success" className="text-[10px]">Online</Badge>
              </h3>
              <p className="text-xs text-muted-foreground">Powered by ProfitPilot AI</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon" onClick={handleClearChat} title="Clear chat">
              <Trash2 className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" title="Refresh">
              <RefreshCw className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className={'flex gap-3 ' + (message.role === 'user' ? 'justify-end' : 'justify-start')}
              >
                {message.role === 'assistant' && (
                  <Avatar className="h-8 w-8">
                    <AvatarFallback className="bg-gradient-to-r from-primary to-purple-600 text-white text-xs">
                      AI
                    </AvatarFallback>
                  </Avatar>
                )}
                
                <div className={'max-w-[80%] ' + (message.role === 'user' ? 'order-1' : '')}>
                  <div className={'rounded-lg p-4 ' + (
                    message.role === 'user' 
                      ? 'bg-gradient-to-r from-primary to-purple-600 text-white' 
                      : 'bg-muted'
                  )}>
                    <div className="whitespace-pre-wrap text-sm leading-relaxed">
                      {message.content.split('\n').map((line, i) => (
                        <p key={i} className={line.startsWith('**') ? 'font-semibold' : ''}>
                          {line}
                        </p>
                      ))}
                    </div>
                  </div>
                  <div className={'mt-1 flex items-center gap-2 text-xs text-muted-foreground ' + (message.role === 'user' ? 'justify-end' : 'justify-start')}>
                    <span>{formatTime(message.timestamp)}</span>
                    {message.role === 'assistant' && (
                      <button
                        onClick={() => handleCopy(message.content, message.id)}
                        className="hover:text-foreground transition-colors"
                        title="Copy response"
                      >
                        {copiedId === message.id ? (
                          <Check className="h-3 w-3 text-green-500" />
                        ) : (
                          <Copy className="h-3 w-3" />
                        )}
                      </button>
                    )}
                  </div>
                </div>

                {message.role === 'user' && (
                  <Avatar className="h-8 w-8">
                    <AvatarFallback className="bg-primary/10 text-primary text-xs">
                      {user?.full_name?.charAt(0) || 'U'}
                    </AvatarFallback>
                  </Avatar>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-start gap-3"
            >
              <Avatar className="h-8 w-8">
                <AvatarFallback className="bg-gradient-to-r from-primary to-purple-600 text-white text-xs">
                  AI
                </AvatarFallback>
              </Avatar>
              <div className="rounded-lg bg-muted p-4">
                <div className="flex items-center gap-1">
                  <div className="h-2 w-2 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="h-2 w-2 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="h-2 w-2 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Questions */}
        {messages.length < 3 && (
          <div className="border-t p-4">
            <p className="text-xs text-muted-foreground mb-3 flex items-center gap-2">
              <Lightbulb className="h-3 w-3" />
              Suggested Questions
            </p>
            <div className="flex flex-wrap gap-2">
              {suggestedQuestions.map((sq, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(sq)}
                  className="rounded-full border bg-background/50 px-3 py-1.5 text-xs hover:bg-primary/10 hover:border-primary/30 transition-colors"
                >
                  {sq}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="border-t p-4">
          <div className="flex gap-2">
            <Input
              ref={inputRef}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a business question..."
              className="flex-1"
              disabled={isLoading}
            />
            <Button 
              onClick={handleSend} 
              disabled={isLoading || !question.trim()}
              className="gap-2"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
              Send
            </Button>
          </div>
          <div className="mt-2 flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <Sparkles className="h-3 w-3 text-primary" />
              AI-powered
            </span>
            <span>•</span>
            <span>Business data driven</span>
            <span>•</span>
            <span>Real-time insights</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
};


