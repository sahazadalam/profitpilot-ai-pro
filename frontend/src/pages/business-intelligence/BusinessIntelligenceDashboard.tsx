import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { 
  Brain, TrendingUp, TrendingDown, Shield, Users, 
  BarChart3, Activity, Clock, CheckCircle, AlertTriangle,
  Sparkles, Zap, Target, Award, Globe, RefreshCw,
  Lightbulb, Rocket, Crown, Medal, Trophy, UserCheck,
  UserX, Building2, Briefcase, DollarSign, Package, 
  ShoppingCart, LineChart as LineChartIcon
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Progress } from '@/components/ui/Progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import { api } from '@/services/api';
import toast from 'react-hot-toast';
import {
  PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend, RadarChart,
  PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  AreaChart, Area, LineChart, Line, BarChart, Bar
} from 'recharts';

export const BusinessIntelligenceDashboard = () => {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [selectedTimeframe, setSelectedTimeframe] = useState('30d');
  const [activeTab, setActiveTab] = useState('overview');

  // Fetch customer segments
  const { data: segments, isLoading: segmentsLoading } = useQuery({
    queryKey: ['intelligence', 'segments'],
    queryFn: async () => {
      try {
        const response = await api.get('/intelligence/customer-segments');
        return response.data.data || [];
      } catch (error) {
        console.error('Segments error:', error);
        return [];
      }
    },
    staleTime: 5 * 60 * 1000,
  });

  // Fetch anomalies
  const { data: anomalies } = useQuery({
    queryKey: ['intelligence', 'anomalies'],
    queryFn: async () => {
      try {
        const response = await api.get('/intelligence/anomalies');
        return response.data.data || [];
      } catch (error) {
        console.error('Anomalies error:', error);
        return [];
      }
    },
    staleTime: 5 * 60 * 1000,
  });

  // Fetch market trends
  const { data: marketTrends } = useQuery({
    queryKey: ['intelligence', 'market-trends'],
    queryFn: async () => {
      try {
        const response = await api.get('/intelligence/market-trends');
        return response.data.data || {};
      } catch (error) {
        console.error('Market trends error:', error);
        return {};
      }
    },
    staleTime: 5 * 60 * 1000,
  });

  // Fetch risk prediction
  const { data: riskData } = useQuery({
    queryKey: ['intelligence', 'risk'],
    queryFn: async () => {
      try {
        const response = await api.get('/intelligence/risk-prediction');
        return response.data.data || {};
      } catch (error) {
        console.error('Risk data error:', error);
        return {};
      }
    },
    staleTime: 5 * 60 * 1000,
  });

  // Fetch AI insights
  const { data: insights } = useQuery({
    queryKey: ['intelligence', 'insights'],
    queryFn: async () => {
      try {
        const response = await api.get('/intelligence/insights');
        return response.data.data || [];
      } catch (error) {
        console.error('Insights error:', error);
        return [];
      }
    },
    staleTime: 5 * 60 * 1000,
  });

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    toast.success('Data refreshed!');
    setIsRefreshing(false);
  };

  // Prepare chart data
  const segmentData = Array.isArray(segments) ? segments.map((s: any) => ({
    name: s.segment_name || 'Unknown',
    value: s.customer_count || 0,
    revenue: s.total_revenue || 0,
  })) : [];

  const COLORS = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899'];

  const riskFactors = riskData?.risk_factors || {};
  const radarData = [
    { subject: 'Inventory', A: riskFactors.inventory_risk || 0, fullMark: 100 },
    { subject: 'Revenue', A: riskFactors.revenue_risk || 0, fullMark: 100 },
    { subject: 'Profit', A: riskFactors.profit_risk || 0, fullMark: 100 },
    { subject: 'Concentration', A: riskFactors.concentration_risk || 0, fullMark: 100 },
    { subject: 'Forecast', A: riskFactors.forecast_risk || 0, fullMark: 100 },
  ];

  const insightCards = [
    { icon: Brain, label: 'AI Insights', value: insights?.length || 0, change: '+3 new today', color: 'from-blue-500 to-cyan-500' },
    { icon: Shield, label: 'Risk Level', value: riskData?.risk_level || 'Medium', score: riskData?.risk_score || 65, color: 'from-red-500 to-pink-500' },
    { icon: TrendingUp, label: 'Market Trend', value: marketTrends?.overall_market?.market_trend || 'Growing', change: '+8.5% this month', color: 'from-green-500 to-emerald-500' },
    { icon: Users, label: 'Segments', value: segments?.length || 0, change: 'Customer segments', color: 'from-purple-500 to-indigo-500' },
  ];

  if (segmentsLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6 p-6"
    >
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Business Intelligence</h1>
          <p className="text-muted-foreground">AI-powered insights and intelligence</p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 rounded-lg border bg-background/50 p-1">
            <button
              className={'rounded-md px-3 py-1 text-sm transition-colors ' + (selectedTimeframe === '7d' ? 'bg-primary text-white' : 'hover:bg-muted')}
              onClick={() => setSelectedTimeframe('7d')}
            >
              7D
            </button>
            <button
              className={'rounded-md px-3 py-1 text-sm transition-colors ' + (selectedTimeframe === '30d' ? 'bg-primary text-white' : 'hover:bg-muted')}
              onClick={() => setSelectedTimeframe('30d')}
            >
              30D
            </button>
            <button
              className={'rounded-md px-3 py-1 text-sm transition-colors ' + (selectedTimeframe === '90d' ? 'bg-primary text-white' : 'hover:bg-muted')}
              onClick={() => setSelectedTimeframe('90d')}
            >
              90D
            </button>
          </div>
          <Button variant="outline" size="sm" className="gap-2" onClick={handleRefresh} disabled={isRefreshing}>
            <RefreshCw className={'h-4 w-4 ' + (isRefreshing ? 'animate-spin' : '')} />
            Refresh
          </Button>
        </div>
      </div>

      {/* Insight Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {insightCards.map((card, index) => (
          <motion.div
            key={card.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <Card className="relative overflow-hidden border-0 bg-gradient-to-br shadow-lg">
              <div className={'absolute inset-0 bg-gradient-to-br ' + card.color + ' opacity-10'} />
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">{card.label}</p>
                    <p className="text-2xl font-bold">
                      {typeof card.value === 'number' ? card.value : card.value}
                    </p>
                    {card.change && (
                      <p className="text-xs text-muted-foreground">{card.change}</p>
                    )}
                    {card.score && (
                      <div className="mt-2">
                        <Progress value={card.score} className="h-1.5" />
                        <p className="text-xs text-muted-foreground mt-1">Score: {card.score}/100</p>
                      </div>
                    )}
                  </div>
                  <div className={'rounded-lg bg-gradient-to-br ' + card.color + ' p-3 text-white'}>
                    <card.icon className="h-6 w-6" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="segments">Segments</TabsTrigger>
          <TabsTrigger value="risks">Risks</TabsTrigger>
          <TabsTrigger value="trends">Trends</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            {/* Customer Segments Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Customer Segments
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  {segmentData.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={segmentData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, percent }) => name + ' ' + (percent * 100).toFixed(0) + '%'}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {segmentData.map((entry: any, index: number) => (
                            <Cell key={'cell-' + index} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip
                          contentStyle={{
                            background: 'var(--background)',
                            border: '1px solid var(--border)',
                            borderRadius: '8px',
                          }}
                        />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="flex h-full items-center justify-center text-muted-foreground">
                      No segment data available
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Risk Radar */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Risk Assessment
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="subject" />
                      <PolarRadiusAxis angle={30} domain={[0, 100]} />
                      <Radar name="Risk Score" dataKey="A" stroke="#ef4444" fill="#ef4444" fillOpacity={0.3} />
                      <Tooltip
                        contentStyle={{
                          background: 'var(--background)',
                          border: '1px solid var(--border)',
                          borderRadius: '8px',
                        }}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* AI Insights */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Lightbulb className="h-5 w-5 text-yellow-500" />
                AI Insights
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                {Array.isArray(insights) && insights.length > 0 ? (
                  insights.slice(0, 4).map((insight: any, index: number) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.1 }}
                      className="flex items-start gap-3 rounded-lg border p-4 hover:bg-muted/50 transition-colors"
                    >
                      <div className={'rounded-full p-2 ' + (insight.type === 'positive' ? 'bg-green-500/10' : insight.type === 'negative' ? 'bg-red-500/10' : 'bg-yellow-500/10')}>
                        {insight.type === 'positive' ? (
                          <CheckCircle className="h-4 w-4 text-green-500" />
                        ) : insight.type === 'negative' ? (
                          <AlertTriangle className="h-4 w-4 text-red-500" />
                        ) : (
                          <AlertTriangle className="h-4 w-4 text-yellow-500" />
                        )}
                      </div>
                      <div className="flex-1">
                        <p className="text-sm">{insight.message}</p>
                        <p className="text-xs text-muted-foreground">{insight.category}</p>
                      </div>
                      <Badge variant={insight.priority === 'high' ? 'destructive' : insight.priority === 'medium' ? 'default' : 'secondary'}>
                        {insight.priority}
                      </Badge>
                    </motion.div>
                  ))
                ) : (
                  <div className="col-span-2 text-center py-8 text-muted-foreground">
                    No insights available
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="segments" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {segmentData.map((segment: any, index: number) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <Card className="hover:shadow-lg transition-all">
                  <CardContent className="p-6">
                    <div className="flex items-center gap-3">
                      <div className={'rounded-lg p-2 bg-gradient-to-br ' + (index % 2 === 0 ? 'from-blue-500 to-cyan-500' : 'from-purple-500 to-pink-500')}>
                        <Users className="h-5 w-5 text-white" />
                      </div>
                      <div>
                        <p className="font-medium">{segment.name}</p>
                        <p className="text-sm text-muted-foreground">{segment.value} customers</p>
                      </div>
                    </div>
                    <div className="mt-4">
                      <Progress value={segment.value / 10} className="h-2" />
                    </div>
                    <div className="mt-4 flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Revenue</span>
                      <span className="font-medium"></span>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="risks" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Risk Breakdown
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {Object.entries(riskFactors).map(([key, value]: [string, any]) => (
                  <div key={key}>
                    <div className="flex items-center justify-between">
                      <span className="text-sm capitalize">{key.replace('_', ' ')}</span>
                      <span className="text-sm font-medium">{value}/100</span>
                    </div>
                    <Progress value={value} className="h-2" />
                  </div>
                ))}
                {Object.keys(riskFactors).length === 0 && (
                  <div className="text-center py-8 text-muted-foreground">
                    No risk data available
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5" />
                  Risk Recommendations
                </CardTitle>
              </CardHeader>
              <CardContent>
                {riskData?.recommendations?.length > 0 ? (
                  <div className="space-y-3">
                    {riskData.recommendations.map((rec: string, index: number) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.1 }}
                        className="flex items-start gap-3 rounded-lg border p-3"
                      >
                        <div className="rounded-full bg-yellow-500/10 p-1.5">
                          <AlertTriangle className="h-4 w-4 text-yellow-500" />
                        </div>
                        <p className="text-sm">{rec}</p>
                      </motion.div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    No risk recommendations available
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="trends" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Market Trends
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                {marketTrends?.industries && Object.entries(marketTrends.industries).map(([key, value]: [string, any]) => (
                  <motion.div
                    key={key}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                    className="rounded-lg border p-4"
                  >
                    <div className="flex items-center justify-between">
                      <h4 className="font-medium capitalize">{key}</h4>
                      <Badge variant={value.growth_rate > 0 ? 'success' : 'secondary'}>
                        {value.growth_rate > 0 ? '+' : ''}{value.growth_rate}%
                      </Badge>
                    </div>
                    <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
                      <div>
                        <p className="text-muted-foreground">Demand</p>
                        <p className="font-medium">{value.expected_demand?.toFixed(0) || 0}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Risk</p>
                        <p className="font-medium">{value.risk_score?.toFixed(0) || 0}%</p>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </motion.div>
  );
};

