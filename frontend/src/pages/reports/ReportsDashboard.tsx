import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import { 
  Download, 
  FileText, 
  Calendar, 
  RefreshCw,
  Share2,
  Printer,
  TrendingUp,
  TrendingDown,
  DollarSign,
  ShoppingBag,
  Users,
  Eye,
  Clock,
  Star,
  AlertCircle,
  BarChart3,
  PieChart,
  ChevronRight
} from 'lucide-react';
import { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart as RePieChart,
  Pie,
  Cell
} from 'recharts';

type Period = 'daily' | 'weekly' | 'monthly' | 'quarterly' | 'yearly';

interface MetricData {
  revenue: string;
  orders: string;
  conversion: string;
  aov: string;
  growth: string;
}

interface ChartData {
  labels: string[];
  revenue: number[];
  orders: number[];
}

interface Order {
  id: string;
  customer: string;
  amount: string;
  status: 'completed' | 'pending' | 'processing' | 'cancelled';
  date: string;
}

interface TopProduct {
  name: string;
  units: number;
  revenue: string;
  growth: number;
}

export const ReportsDashboard = () => {
  const [activePeriod, setActivePeriod] = useState<Period>('daily');
  const [isLoading, setIsLoading] = useState(false);
  const [reportData, setReportData] = useState<ChartData | null>(null);
  const [metrics, setMetrics] = useState<MetricData | null>(null);
  const [recentOrders, setRecentOrders] = useState<Order[]>([]);
  const [topProducts, setTopProducts] = useState<TopProduct[]>([]);

  // Sample data for different periods
  const chartDataMap: Record<Period, ChartData> = {
    daily: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      revenue: [3200, 4100, 3800, 5200, 4900, 6100, 5800],
      orders: [45, 52, 48, 67, 58, 72, 65]
    },
    weekly: {
      labels: ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7'],
      revenue: [18500, 21200, 19800, 24300, 22900, 27100, 25800],
      orders: [210, 245, 228, 278, 256, 298, 285]
    },
    monthly: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
      revenue: [68200, 71900, 75800, 82300, 87900, 93400, 98200],
      orders: [780, 820, 856, 912, 968, 1024, 1085]
    },
    quarterly: {
      labels: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'],
      revenue: [215000, 238000, 256000, 289000, 312000, 334000],
      orders: [2400, 2650, 2820, 3120, 3350, 3580]
    },
    yearly: {
      labels: ['2019', '2020', '2021', '2022', '2023', '2024', '2025'],
      revenue: [820000, 895000, 978000, 1050000, 1140000, 1230000, 1320000],
      orders: [9200, 9850, 10750, 11500, 12400, 13250, 14100]
    }
  };

  const metricsMap: Record<Period, MetricData> = {
    daily: {
      revenue: '$48,250',
      orders: '342',
      conversion: '4.8%',
      aov: '$141',
      growth: '+12.5%'
    },
    weekly: {
      revenue: '$312,400',
      orders: '2,184',
      conversion: '5.2%',
      aov: '$143',
      growth: '+8.3%'
    },
    monthly: {
      revenue: '$1,283,700',
      orders: '8,926',
      conversion: '5.6%',
      aov: '$144',
      growth: '+9.7%'
    },
    quarterly: {
      revenue: '$3,847,200',
      orders: '26,410',
      conversion: '5.9%',
      aov: '$146',
      growth: '+11.2%'
    },
    yearly: {
      revenue: '$14,928,000',
      orders: '98,720',
      conversion: '6.2%',
      aov: '$151',
      growth: '+13.8%'
    }
  };

  // Mock orders data
  const getOrders = (period: Period): Order[] => {
    const baseOrders: Order[] = [
      { id: '#1042', customer: 'Sarah Johnson', amount: '$245.00', status: 'completed', date: '2026-07-25' },
      { id: '#1041', customer: 'Mike Chen', amount: '$189.50', status: 'pending', date: '2026-07-25' },
      { id: '#1040', customer: 'Emily Davis', amount: '$432.00', status: 'completed', date: '2026-07-24' },
      { id: '#1039', customer: 'James Wilson', amount: '$156.75', status: 'completed', date: '2026-07-24' },
      { id: '#1038', customer: 'Lisa Park', amount: '$278.30', status: 'pending', date: '2026-07-23' },
      { id: '#1037', customer: 'Robert Martinez', amount: '$621.00', status: 'processing', date: '2026-07-23' },
      { id: '#1036', customer: 'Amanda Lee', amount: '$194.20', status: 'completed', date: '2026-07-22' },
      { id: '#1035', customer: 'David Kim', amount: '$345.80', status: 'cancelled', date: '2026-07-22' }
    ];
    
    const count = period === 'daily' ? 5 : period === 'weekly' ? 7 : period === 'monthly' ? 8 : 8;
    return baseOrders.slice(0, count);
  };

  // Mock top products
  const getTopProducts = (period: Period): TopProduct[] => {
    return [
      { name: 'Pro Headset', units: 87, revenue: '$13,050', growth: 15.2 },
      { name: 'Ultra Monitor', units: 62, revenue: '$18,600', growth: 8.7 },
      { name: 'Wireless Mouse', units: 54, revenue: '$3,780', growth: -2.3 },
      { name: 'Mechanical KB', units: 41, revenue: '$4,510', growth: 12.1 },
      { name: 'USB-C Hub', units: 38, revenue: '$3,420', growth: 5.6 }
    ];
  };

  // Load data when period changes
  useEffect(() => {
    loadReportData(activePeriod);
  }, [activePeriod]);

  const loadReportData = (period: Period) => {
    setIsLoading(true);
    setTimeout(() => {
      setReportData(chartDataMap[period]);
      setMetrics(metricsMap[period]);
      setRecentOrders(getOrders(period));
      setTopProducts(getTopProducts(period));
      setIsLoading(false);
    }, 600);
  };

  const handleRefresh = () => {
    loadReportData(activePeriod);
  };

  const handleDownload = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      const periodNames = {
        daily: 'Daily',
        weekly: 'Weekly',
        monthly: 'Monthly',
        quarterly: 'Quarterly',
        yearly: 'Yearly'
      };
      alert(`✅ ${periodNames[activePeriod]} Report downloaded successfully!\n\n📊 Includes revenue, orders, conversion rates, and top products.\n📁 Format: PDF with full charts and metrics.`);
    }, 1500);
  };

  const handleShare = () => {
    navigator.clipboard?.writeText('https://profitpilot.ai/reports/' + activePeriod);
    alert('📤 Share link copied to clipboard!');
  };

  const handlePrint = () => {
    window.print();
  };

  const getStatusColor = (status: Order['status']) => {
    const colors = {
      completed: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      processing: 'bg-blue-100 text-blue-800',
      cancelled: 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getStatusDot = (status: Order['status']) => {
    const colors = {
      completed: 'bg-green-500',
      pending: 'bg-yellow-500',
      processing: 'bg-blue-500',
      cancelled: 'bg-red-500'
    };
    return colors[status] || 'bg-gray-500';
  };

  const formatDate = () => {
    const now = new Date();
    return now.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  // Prepare chart data
  const prepareLineData = () => {
    if (!reportData) return [];
    return reportData.labels.map((label, index) => ({
      name: label,
      Revenue: reportData.revenue[index],
      Orders: reportData.orders[index] * 100
    }));
  };

  const pieData = [
    { name: 'Completed', value: 65 },
    { name: 'Pending', value: 20 },
    { name: 'Processing', value: 10 },
    { name: 'Cancelled', value: 5 }
  ];

  const COLORS = ['#4CAF50', '#FFC107', '#2196F3', '#F44336'];

  const periodNames = {
    daily: 'Daily',
    weekly: 'Weekly',
    monthly: 'Monthly',
    quarterly: 'Quarterly',
    yearly: 'Yearly'
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6 p-6"
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Reports</h1>
          <p className="text-muted-foreground">Generate and manage business reports</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" size="sm" className="gap-2" onClick={handleRefresh}>
            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button variant="outline" size="sm" className="gap-2" onClick={handleShare}>
            <Share2 className="h-4 w-4" />
            Share
          </Button>
          <Button variant="outline" size="sm" className="gap-2" onClick={handlePrint}>
            <Printer className="h-4 w-4" />
            Print
          </Button>
          <Button variant="outline" size="sm" className="gap-2" onClick={handleDownload}>
            <Download className="h-4 w-4" />
            Download
          </Button>
          <Button size="sm" className="gap-2">
            <FileText className="h-4 w-4" />
            Generate Report
          </Button>
        </div>
      </div>

      {/* Date Badge */}
      <div className="flex items-center gap-2 text-sm text-muted-foreground bg-muted/50 px-4 py-2 rounded-lg w-fit">
        <Calendar className="h-4 w-4" />
        <span>{formatDate()}</span>
      </div>

      <Tabs 
        defaultValue="daily" 
        className="space-y-4"
        onValueChange={(value) => setActivePeriod(value as Period)}
      >
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="daily">Daily</TabsTrigger>
          <TabsTrigger value="weekly">Weekly</TabsTrigger>
          <TabsTrigger value="monthly">Monthly</TabsTrigger>
          <TabsTrigger value="quarterly">Quarterly</TabsTrigger>
          <TabsTrigger value="yearly">Yearly</TabsTrigger>
        </TabsList>

        {(['daily', 'weekly', 'monthly', 'quarterly', 'yearly'] as Period[]).map((period) => (
          <TabsContent key={period} value={period}>
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Calendar className="h-5 w-5" />
                    {periodNames[period]} Report
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-80">
                      <div className="text-center">
                        <RefreshCw className="h-12 w-12 text-primary animate-spin mx-auto mb-4" />
                        <p className="text-muted-foreground">Loading report data...</p>
                      </div>
                    </div>
                  ) : (
                    <>
                      {/* Charts Section */}
                      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <div className="lg:col-span-2">
                          <h3 className="text-sm font-medium text-muted-foreground mb-4 flex items-center gap-2">
                            <BarChart3 className="h-4 w-4" />
                            Revenue & Orders Trend
                          </h3>
                          <div className="h-64">
                            <ResponsiveContainer width="100%" height="100%">
                              <LineChart data={prepareLineData()}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                                <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
                                <YAxis stroke="#9ca3af" fontSize={12} />
                                <Tooltip
                                  contentStyle={{
                                    backgroundColor: 'white',
                                    border: '1px solid #e5e7eb',
                                    borderRadius: '8px'
                                  }}
                                />
                                <Legend />
                                <Line
                                  type="monotone"
                                  dataKey="Revenue"
                                  stroke="#3B82F6"
                                  strokeWidth={3}
                                  dot={{ fill: '#3B82F6', strokeWidth: 2 }}
                                />
                                <Line
                                  type="monotone"
                                  dataKey="Orders"
                                  stroke="#10B981"
                                  strokeWidth={3}
                                  dot={{ fill: '#10B981', strokeWidth: 2 }}
                                />
                              </LineChart>
                            </ResponsiveContainer>
                          </div>
                        </div>

                        <div>
                          <h3 className="text-sm font-medium text-muted-foreground mb-4 flex items-center gap-2">
                            <PieChart className="h-4 w-4" />
                            Order Distribution
                          </h3>
                          <div className="h-64">
                            <ResponsiveContainer width="100%" height="100%">
                              <RePieChart>
                                <Pie
                                  data={pieData}
                                  cx="50%"
                                  cy="50%"
                                  innerRadius={60}
                                  outerRadius={80}
                                  paddingAngle={5}
                                  dataKey="value"
                                >
                                  {pieData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                  ))}
                                </Pie>
                                <Tooltip />
                                <Legend />
                              </RePieChart>
                            </ResponsiveContainer>
                          </div>
                        </div>
                      </div>

                      {/* Metrics Grid */}
                      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                        <div className="bg-blue-50 dark:bg-blue-950/30 rounded-lg p-4 border border-blue-100 dark:border-blue-800">
                          <div className="flex items-center gap-2 text-sm text-blue-700 dark:text-blue-400 mb-1">
                            <DollarSign className="h-4 w-4" />
                            <span>Revenue</span>
                          </div>
                          <div className="text-2xl font-bold text-blue-900 dark:text-blue-100">
                            {metrics?.revenue || '$0'}
                          </div>
                          <div className="flex items-center gap-1 text-sm text-green-600 mt-1">
                            <TrendingUp className="h-3 w-3" />
                            <span>{metrics?.growth || '+0%'}</span>
                          </div>
                        </div>

                        <div className="bg-purple-50 dark:bg-purple-950/30 rounded-lg p-4 border border-purple-100 dark:border-purple-800">
                          <div className="flex items-center gap-2 text-sm text-purple-700 dark:text-purple-400 mb-1">
                            <ShoppingBag className="h-4 w-4" />
                            <span>Orders</span>
                          </div>
                          <div className="text-2xl font-bold text-purple-900 dark:text-purple-100">
                            {metrics?.orders || '0'}
                          </div>
                          <div className="flex items-center gap-1 text-sm text-green-600 mt-1">
                            <TrendingUp className="h-3 w-3" />
                            <span>+8.3%</span>
                          </div>
                        </div>

                        <div className="bg-green-50 dark:bg-green-950/30 rounded-lg p-4 border border-green-100 dark:border-green-800">
                          <div className="flex items-center gap-2 text-sm text-green-700 dark:text-green-400 mb-1">
                            <Users className="h-4 w-4" />
                            <span>Conversion</span>
                          </div>
                          <div className="text-2xl font-bold text-green-900 dark:text-green-100">
                            {metrics?.conversion || '0%'}
                          </div>
                          <div className="flex items-center gap-1 text-sm text-red-600 mt-1">
                            <TrendingDown className="h-3 w-3" />
                            <span>-0.6%</span>
                          </div>
                        </div>

                        <div className="bg-orange-50 dark:bg-orange-950/30 rounded-lg p-4 border border-orange-100 dark:border-orange-800">
                          <div className="flex items-center gap-2 text-sm text-orange-700 dark:text-orange-400 mb-1">
                            <DollarSign className="h-4 w-4" />
                            <span>Average Order</span>
                          </div>
                          <div className="text-2xl font-bold text-orange-900 dark:text-orange-100">
                            {metrics?.aov || '$0'}
                          </div>
                          <div className="flex items-center gap-1 text-sm text-green-600 mt-1">
                            <TrendingUp className="h-3 w-3" />
                            <span>+3.2%</span>
                          </div>
                        </div>

                        <div className="bg-indigo-50 dark:bg-indigo-950/30 rounded-lg p-4 border border-indigo-100 dark:border-indigo-800">
                          <div className="flex items-center gap-2 text-sm text-indigo-700 dark:text-indigo-400 mb-1">
                            <Eye className="h-4 w-4" />
                            <span>Visitors</span>
                          </div>
                          <div className="text-2xl font-bold text-indigo-900 dark:text-indigo-100">
                            4,231
                          </div>
                          <div className="flex items-center gap-1 text-sm text-green-600 mt-1">
                            <TrendingUp className="h-3 w-3" />
                            <span>+5.7%</span>
                          </div>
                        </div>
                      </div>

                      {/* Recent Orders and Top Products */}
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <div>
                          <h3 className="text-sm font-medium text-muted-foreground mb-4 flex items-center gap-2">
                            <Clock className="h-4 w-4" />
                            Recent Orders
                          </h3>
                          <div className="space-y-2 max-h-64 overflow-y-auto">
                            {recentOrders.map((order) => (
                              <div
                                key={order.id}
                                className="flex items-center justify-between p-3 rounded-lg border bg-card hover:shadow-sm transition-shadow"
                              >
                                <div className="flex items-center gap-3">
                                  <div className={`h-2 w-2 rounded-full ${getStatusDot(order.status)}`} />
                                  <div>
                                    <div className="font-medium">{order.id}</div>
                                    <div className="text-sm text-muted-foreground">{order.customer}</div>
                                  </div>
                                </div>
                                <div className="text-right">
                                  <div className="font-semibold">{order.amount}</div>
                                  <span className={`inline-block px-2 py-0.5 text-xs font-medium rounded-full ${getStatusColor(order.status)}`}>
                                    {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                                  </span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div>
                          <h3 className="text-sm font-medium text-muted-foreground mb-4 flex items-center gap-2">
                            <Star className="h-4 w-4 text-yellow-500" />
                            Top Products
                          </h3>
                          <div className="space-y-2">
                            {topProducts.map((product, index) => (
                              <div
                                key={index}
                                className="flex items-center justify-between p-3 rounded-lg border bg-card hover:shadow-sm transition-shadow"
                              >
                                <div className="flex items-center gap-3">
                                  <span className="w-6 h-6 flex items-center justify-center bg-primary/10 text-primary rounded-full text-xs font-bold">
                                    {index + 1}
                                  </span>
                                  <div>
                                    <div className="font-medium">{product.name}</div>
                                    <div className="text-sm text-muted-foreground">{product.units} units</div>
                                  </div>
                                </div>
                                <div className="text-right">
                                  <div className="font-semibold">{product.revenue}</div>
                                  <div className={`text-sm ${product.growth >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                    {product.growth >= 0 ? '+' : ''}{product.growth}%
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      {/* AI Insights */}
                      <div className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30 rounded-lg border border-blue-100 dark:border-blue-800">
                        <div className="flex items-start gap-3">
                          <AlertCircle className="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
                          <div>
                            <h4 className="font-semibold text-blue-900 dark:text-blue-100">AI Insights</h4>
                            <p className="text-sm text-blue-800 dark:text-blue-300 mt-1">
                              📈 Revenue is trending {parseFloat(metrics?.growth || '0') > 10 ? 'strongly' : 'steadily'} upward. 
                              Consider increasing inventory for top products: {topProducts.slice(0, 2).map(p => p.name).join(' & ')}.
                              Conversion rate could be improved by 0.8% with targeted promotions.
                            </p>
                          </div>
                        </div>
                      </div>

                      <div className="flex justify-end">
                        <Button variant="ghost" size="sm" className="gap-1">
                          View Full Report
                          <ChevronRight className="h-4 w-4" />
                        </Button>
                      </div>
                    </>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          </TabsContent>
        ))}
      </Tabs>
    </motion.div>
  );
};