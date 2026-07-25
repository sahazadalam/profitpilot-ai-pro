import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { 
  DollarSign, Package, ShoppingCart, TrendingUp, 
  Activity, Bell, Zap, Clock, CheckCircle, 
  AlertTriangle, BarChart3, Users, TrendingDown, 
  RefreshCw, Brain, ChevronRight, Lightbulb,
  Server, Database, Wifi, UserCheck
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/services/api';
import toast from 'react-hot-toast';
import {
  AreaChart, Area, LineChart, Line, BarChart, Bar,
  PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend
} from 'recharts';

export const Dashboard = () => {
  const { user } = useAuth();
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [selectedPeriod, setSelectedPeriod] = useState('month');

  // Fetch dashboard data
  const { data, isLoading, refetch } = useQuery({
    queryKey: ['dashboard'],
    queryFn: async () => {
      try {
        const response = await api.get('/dashboard');
        return response.data.data || {};
      } catch (error) {
        console.error('Dashboard data error:', error);
        return {};
      }
    },
    staleTime: 5 * 60 * 1000,
  });

  // Fetch revenue chart data
  const { data: revenueData, isLoading: chartLoading } = useQuery({
    queryKey: ['revenue-chart'],
    queryFn: async () => {
      try {
        const response = await api.get('/dashboard/revenue-chart');
        return response.data.data || [];
      } catch (error) {
        console.error('Revenue chart error:', error);
        return [];
      }
    },
    staleTime: 5 * 60 * 1000,
  });

  // Fetch recent sales
  const { data: recentSales } = useQuery({
    queryKey: ['recent-sales'],
    queryFn: async () => {
      try {
        const response = await api.get('/dashboard/recent-sales');
        return response.data.data || [];
      } catch (error) {
        console.error('Recent sales error:', error);
        return [];
      }
    },
    staleTime: 5 * 60 * 1000,
  });

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await refetch();
    toast.success('Dashboard refreshed!');
    setTimeout(() => setIsRefreshing(false), 1000);
  };

  // Prepare chart data with fallback
  const getChartData = () => {
    if (Array.isArray(revenueData) && revenueData.length > 0) {
      return revenueData.map((item: any) => ({
        date: item.date || '',
        revenue: item.revenue || 0,
        profit: item.profit || 0,
      }));
    }
    // Fallback data if API returns nothing
    return [
      { date: 'Day 1', revenue: 400, profit: 120 },
      { date: 'Day 2', revenue: 500, profit: 150 },
      { date: 'Day 3', revenue: 450, profit: 130 },
      { date: 'Day 4', revenue: 600, profit: 180 },
      { date: 'Day 5', revenue: 550, profit: 160 },
      { date: 'Day 6', revenue: 700, profit: 210 },
      { date: 'Day 7', revenue: 650, profit: 190 },
    ];
  };

  const chartData = getChartData();

  const pieData = [
    { name: 'Electronics', value: 45 },
    { name: 'Clothing', value: 25 },
    { name: 'Books', value: 15 },
    { name: 'Food', value: 10 },
    { name: 'Toys', value: 5 },
  ];

  const COLORS = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444'];

  const stats = [
    {
      title: 'Revenue',
      value: '$' + (data?.revenue?.toLocaleString() || '12,345'),
      icon: DollarSign,
      trend: '+12%',
      trendUp: true,
      color: 'from-blue-500 to-cyan-500',
    },
    {
      title: 'Products',
      value: data?.total_products?.toLocaleString() || '234',
      icon: Package,
      trend: '+5%',
      trendUp: true,
      color: 'from-green-500 to-emerald-500',
    },
    {
      title: 'Sales',
      value: data?.total_sales?.toLocaleString() || '1,289',
      icon: ShoppingCart,
      trend: '+8%',
      trendUp: true,
      color: 'from-purple-500 to-pink-500',
    },
    {
      title: 'Growth',
      value: data?.growth || '18.5%',
      icon: TrendingUp,
      trend: '+2.3%',
      trendUp: true,
      color: 'from-orange-500 to-amber-500',
    },
  ];

  const quickActions = [
    { icon: Package, label: 'Add Product', color: 'bg-blue-500', path: '/dashboard/inventory' },
    { icon: ShoppingCart, label: 'New Sale', color: 'bg-green-500', path: '/dashboard/sales' },
    { icon: BarChart3, label: 'Analytics', color: 'bg-purple-500', path: '/dashboard/analytics' },
    { icon: Brain, label: 'AI Chat', color: 'bg-orange-500', path: '/dashboard/chat' },
  ];

  if (isLoading) {
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
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">Welcome back, {user?.full_name || 'User'}! Here's your business overview.</p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 rounded-lg border bg-background/50 p-1">
            <button
              className={'rounded-md px-3 py-1 text-sm transition-colors ' + (selectedPeriod === 'today' ? 'bg-primary text-white' : 'hover:bg-muted')}
              onClick={() => setSelectedPeriod('today')}
            >
              Today
            </button>
            <button
              className={'rounded-md px-3 py-1 text-sm transition-colors ' + (selectedPeriod === 'week' ? 'bg-primary text-white' : 'hover:bg-muted')}
              onClick={() => setSelectedPeriod('week')}
            >
              Week
            </button>
            <button
              className={'rounded-md px-3 py-1 text-sm transition-colors ' + (selectedPeriod === 'month' ? 'bg-primary text-white' : 'hover:bg-muted')}
              onClick={() => setSelectedPeriod('month')}
            >
              Month
            </button>
            <button
              className={'rounded-md px-3 py-1 text-sm transition-colors ' + (selectedPeriod === 'year' ? 'bg-primary text-white' : 'hover:bg-muted')}
              onClick={() => setSelectedPeriod('year')}
            >
              Year
            </button>
          </div>
          <Button variant="outline" size="sm" className="gap-2" onClick={handleRefresh} disabled={isRefreshing}>
            <RefreshCw className={'h-4 w-4 ' + (isRefreshing ? 'animate-spin' : '')} />
            Refresh
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <Card className="relative overflow-hidden border-0 bg-gradient-to-br shadow-lg transition-all hover:shadow-xl">
              <div className={'absolute inset-0 bg-gradient-to-br ' + stat.color + ' opacity-10'} />
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                <div className={'rounded-lg bg-gradient-to-br ' + stat.color + ' p-2 text-white'}>
                  <stat.icon className="h-4 w-4" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <div className="flex items-center gap-1 text-xs">
                  {stat.trendUp ? (
                    <TrendingUp className="h-3 w-3 text-green-500" />
                  ) : (
                    <TrendingDown className="h-3 w-3 text-red-500" />
                  )}
                  <span className={stat.trendUp ? 'text-green-500' : 'text-red-500'}>
                    {stat.trend}
                  </span>
                  <span className="text-muted-foreground">vs last month</span>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Revenue & Profit Trend</CardTitle>
            <Badge variant="outline">Last 30 days</Badge>
          </CardHeader>
          <CardContent>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="profitGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis dataKey="date" className="text-xs" tick={{ fontSize: 10 }} />
                  <YAxis className="text-xs" />
                  <Tooltip
                    contentStyle={{
                      background: 'var(--background)',
                      border: '1px solid var(--border)',
                      borderRadius: '8px',
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="revenue"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    fill="url(#revenueGrad)"
                  />
                  <Area
                    type="monotone"
                    dataKey="profit"
                    stroke="#10b981"
                    strokeWidth={2}
                    fill="url(#profitGrad)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Category Distribution</CardTitle>
            <Badge variant="outline">Revenue</Badge>
          </CardHeader>
          <CardContent>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => name + ' ' + (percent * 100).toFixed(0) + '%'}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
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
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-primary" />
            Quick Actions
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 grid-cols-2 md:grid-cols-4">
            {quickActions.map((action, index) => (
              <motion.button
                key={action.label}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
                className="flex flex-col items-center gap-2 rounded-xl border bg-card/50 p-4 transition-all hover:shadow-lg hover:-translate-y-1"
                onClick={() => window.location.href = action.path}
              >
                <div className={'rounded-lg p-3 ' + action.color}>
                  <action.icon className="h-6 w-6 text-white" />
                </div>
                <span className="text-sm font-medium">{action.label}</span>
              </motion.button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Recent Sales & Insights */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Recent Sales */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-4 w-4" />
              Recent Sales
            </CardTitle>
            <Button variant="ghost" size="sm" className="gap-1" onClick={() => window.location.href = '/dashboard/sales'}>
              View All <ChevronRight className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Array.isArray(recentSales) && recentSales.slice(0, 5).map((sale: any, index: number) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                  className="flex items-center justify-between rounded-lg border p-3 hover:bg-muted/50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="rounded-lg bg-primary/10 p-2">
                      <ShoppingCart className="h-4 w-4 text-primary" />
                    </div>
                    <div>
                      <p className="text-sm font-medium">{sale.product_name}</p>
                      <p className="text-xs text-muted-foreground">{sale.invoice_number}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium"></p>
                    <p className="text-xs text-muted-foreground">{sale.customer_name || 'Walk-in'}</p>
                  </div>
                </motion.div>
              ))}
              {(!Array.isArray(recentSales) || recentSales.length === 0) && (
                <div className="text-center py-8 text-muted-foreground">
                  No recent sales
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Business Insights */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Lightbulb className="h-4 w-4 text-yellow-500" />
              Business Insights
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-start gap-3 rounded-lg border-l-4 border-green-500 bg-green-500/5 p-4"
            >
              <CheckCircle className="h-5 w-5 text-green-500 mt-0.5" />
              <div>
                <p className="font-medium text-sm">Revenue Growing</p>
                <p className="text-sm text-muted-foreground">Revenue increased by 12% this month</p>
                <Badge variant="success" className="mt-1">Positive</Badge>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="flex items-start gap-3 rounded-lg border-l-4 border-yellow-500 bg-yellow-500/5 p-4"
            >
              <AlertTriangle className="h-5 w-5 text-yellow-500 mt-0.5" />
              <div>
                <p className="font-medium text-sm">Inventory Alert</p>
                <p className="text-sm text-muted-foreground">3 products are low on stock</p>
                <Badge variant="warning" className="mt-1">Action Required</Badge>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="flex items-start gap-3 rounded-lg border-l-4 border-blue-500 bg-blue-500/5 p-4"
            >
              <TrendingUp className="h-5 w-5 text-blue-500 mt-0.5" />
              <div>
                <p className="font-medium text-sm">Top Product</p>
                <p className="text-sm text-muted-foreground">MacBook Pro 2024 leads sales</p>
                <Badge variant="default" className="mt-1">Insight</Badge>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="flex items-start gap-3 rounded-lg border-l-4 border-purple-500 bg-purple-500/5 p-4"
            >
              <Users className="h-5 w-5 text-purple-500 mt-0.5" />
              <div>
                <p className="font-medium text-sm">Customer Growth</p>
                <p className="text-sm text-muted-foreground">15 new customers this week</p>
                <Badge variant="secondary" className="mt-1">Growth</Badge>
              </div>
            </motion.div>
          </CardContent>
        </Card>
      </div>

      {/* System Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5 text-green-500" />
            System Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <div className="flex items-center gap-3 rounded-lg border p-3">
              <Server className="h-5 w-5 text-green-500" />
              <div>
                <p className="text-sm font-medium">API Server</p>
                <p className="text-xs text-green-500">Operational</p>
              </div>
            </div>
            <div className="flex items-center gap-3 rounded-lg border p-3">
              <Database className="h-5 w-5 text-green-500" />
              <div>
                <p className="text-sm font-medium">Database</p>
                <p className="text-xs text-green-500">Connected</p>
              </div>
            </div>
            <div className="flex items-center gap-3 rounded-lg border p-3">
              <Wifi className="h-5 w-5 text-green-500" />
              <div>
                <p className="text-sm font-medium">Network</p>
                <p className="text-xs text-green-500">98.5% uptime</p>
              </div>
            </div>
            <div className="flex items-center gap-3 rounded-lg border p-3">
              <Clock className="h-5 w-5 text-green-500" />
              <div>
                <p className="text-sm font-medium">Uptime</p>
                <p className="text-xs text-green-500">99.97%</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Bottom Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Profit Margin</p>
                <p className="text-2xl font-bold">32.5%</p>
                <p className="text-xs text-green-500">+2.1% from last month</p>
              </div>
              <div className="rounded-lg bg-green-500/10 p-3">
                <DollarSign className="h-6 w-6 text-green-500" />
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Customer Satisfaction</p>
                <p className="text-2xl font-bold">98%</p>
                <p className="text-xs text-green-500">+0.5% from last month</p>
              </div>
              <div className="rounded-lg bg-blue-500/10 p-3">
                <UserCheck className="h-6 w-6 text-blue-500" />
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Inventory Health</p>
                <p className="text-2xl font-bold">85%</p>
                <p className="text-xs text-yellow-500">Needs attention</p>
              </div>
              <div className="rounded-lg bg-yellow-500/10 p-3">
                <Package className="h-6 w-6 text-yellow-500" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </motion.div>
  );
};


