import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { 
  Brain, TrendingUp, TrendingDown, Calendar, 
  BarChart3, Loader2, RefreshCw, AlertCircle,
  LineChart, AreaChart, Activity, Zap,
  Clock, Target, DollarSign, Package
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { api } from '@/services/api';
import toast from 'react-hot-toast';
import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  Bar,
  BarChart
} from 'recharts';

export const PredictionDashboard = () => {
  const [days, setDays] = useState(30);
  const [model, setModel] = useState('prophet');
  const [activeTab, setActiveTab] = useState('forecast');

  // Demand Prediction
  const demandMutation = useMutation({
    mutationFn: async () => {
      const response = await api.post('/predict/demand', { days, model });
      return response.data.data;
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error?.message || 'Failed to predict demand');
    },
  });

  // Revenue Prediction
  const revenueMutation = useMutation({
    mutationFn: async () => {
      const response = await api.post('/predict/revenue', { days, model });
      return response.data.data;
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error?.message || 'Failed to predict revenue');
    },
  });

  // Profit Prediction
  const profitMutation = useMutation({
    mutationFn: async () => {
      const response = await api.post('/predict/profit', { days, model });
      return response.data.data;
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error?.message || 'Failed to predict profit');
    },
  });

  // Inventory Forecast
  const { data: inventoryData, isLoading: inventoryLoading, refetch: refetchInventory } = useQuery({
    queryKey: ['inventory-forecast'],
    queryFn: async () => {
      const response = await api.get('/predict/inventory');
      return response.data.data;
    },
    staleTime: 5 * 60 * 1000,
  });

  // Seasonality
  const { data: seasonalityData, isLoading: seasonalityLoading, refetch: refetchSeasonality } = useQuery({
    queryKey: ['seasonality'],
    queryFn: async () => {
      const response = await api.get('/predict/seasonality');
      return response.data.data;
    },
    staleTime: 5 * 60 * 1000,
  });

  // Moving Average
  const { data: movingAverageData, isLoading: movingAverageLoading, refetch: refetchMovingAverage } = useQuery({
    queryKey: ['moving-average'],
    queryFn: async () => {
      const response = await api.get('/predict/moving-average?window=7');
      return response.data.data;
    },
    staleTime: 5 * 60 * 1000,
  });

  const handlePredictAll = async () => {
    await Promise.all([
      demandMutation.mutateAsync(),
      revenueMutation.mutateAsync(),
      profitMutation.mutateAsync(),
    ]);
    toast.success('All predictions updated!');
  };

  const forecastData = (data: any[]) => {
    if (!data || data.length === 0) return [];
    return data.map(item => ({
      date: item.date || '',
      value: item.value || 0,
      lower: item.lower || 0,
      upper: item.upper || 0,
    }));
  };

  const demandForecast = forecastData(demandMutation.data?.forecast);
  const revenueForecast = forecastData(revenueMutation.data?.forecast);
  const profitForecast = forecastData(profitMutation.data?.forecast);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6 p-6"
    >
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">AI Prediction</h1>
          <p className="text-muted-foreground">Machine learning forecasts and predictions</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <div className="flex items-center gap-2">
            <Input
              type="number"
              value={days}
              onChange={(e) => setDays(parseInt(e.target.value) || 30)}
              className="w-20 h-9"
              min={7}
              max={365}
            />
            <span className="text-sm text-muted-foreground">days</span>
          </div>
          <select
            className="h-9 rounded-md border border-input bg-background px-3 py-1 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="prophet">Prophet</option>
            <option value="arima">ARIMA</option>
            <option value="linear">Linear</option>
          </select>
          <Button size="sm" onClick={handlePredictAll} className="gap-2">
            <RefreshCw className="h-4 w-4" />
            Predict All
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="forecast">Forecasts</TabsTrigger>
          <TabsTrigger value="inventory">Inventory</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="forecast" className="space-y-4">
          {/* Demand Forecast */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <Package className="h-5 w-5 text-primary" />
                  Demand Forecast
                </span>
                <Button 
                  size="sm" 
                  variant="outline" 
                  onClick={() => demandMutation.mutate()}
                  disabled={demandMutation.isPending}
                >
                  {demandMutation.isPending ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    'Predict'
                  )}
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {demandMutation.isPending ? (
                <div className="flex items-center justify-center h-48">
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                </div>
              ) : demandForecast.length > 0 ? (
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <RechartsLineChart data={demandForecast}>
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
                      <Line type="monotone" dataKey="value" stroke="#8b5cf6" strokeWidth={2} dot={false} />
                    </RechartsLineChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="flex h-48 items-center justify-center text-muted-foreground">
                  Click "Predict" to see demand forecast
                </div>
              )}
              {demandMutation.data?.explanation && (
                <p className="mt-2 text-xs text-muted-foreground">{demandMutation.data.explanation}</p>
              )}
            </CardContent>
          </Card>

          {/* Revenue Forecast */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <DollarSign className="h-5 w-5 text-primary" />
                  Revenue Forecast
                </span>
                <Button 
                  size="sm" 
                  variant="outline" 
                  onClick={() => revenueMutation.mutate()}
                  disabled={revenueMutation.isPending}
                >
                  {revenueMutation.isPending ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    'Predict'
                  )}
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {revenueMutation.isPending ? (
                <div className="flex items-center justify-center h-48">
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                </div>
              ) : revenueForecast.length > 0 ? (
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <RechartsLineChart data={revenueForecast}>
                      <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                      <XAxis dataKey="date" className="text-xs" tick={{ fontSize: 10 }} />
                      <YAxis className="text-xs" />
                      <Tooltip
                        contentStyle={{
                          background: 'var(--background)',
                          border: '1px solid var(--border)',
                          borderRadius: '8px',
                        }}
                        formatter={(value) => ['$' + value, 'Revenue']}
                      />
                      <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} dot={false} />
                    </RechartsLineChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="flex h-48 items-center justify-center text-muted-foreground">
                  Click "Predict" to see revenue forecast
                </div>
              )}
              {revenueMutation.data?.explanation && (
                <p className="mt-2 text-xs text-muted-foreground">{revenueMutation.data.explanation}</p>
              )}
            </CardContent>
          </Card>

          {/* Profit Forecast */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-primary" />
                  Profit Forecast
                </span>
                <Button 
                  size="sm" 
                  variant="outline" 
                  onClick={() => profitMutation.mutate()}
                  disabled={profitMutation.isPending}
                >
                  {profitMutation.isPending ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    'Predict'
                  )}
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {profitMutation.isPending ? (
                <div className="flex items-center justify-center h-48">
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                </div>
              ) : profitForecast.length > 0 ? (
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <RechartsLineChart data={profitForecast}>
                      <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                      <XAxis dataKey="date" className="text-xs" tick={{ fontSize: 10 }} />
                      <YAxis className="text-xs" />
                      <Tooltip
                        contentStyle={{
                          background: 'var(--background)',
                          border: '1px solid var(--border)',
                          borderRadius: '8px',
                        }}
                        formatter={(value) => ['$' + value, 'Profit']}
                      />
                      <Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} dot={false} />
                    </RechartsLineChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="flex h-48 items-center justify-center text-muted-foreground">
                  Click "Predict" to see profit forecast
                </div>
              )}
              {profitMutation.data?.explanation && (
                <p className="mt-2 text-xs text-muted-foreground">{profitMutation.data.explanation}</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="inventory" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            {/* Inventory Forecast */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Package className="h-5 w-5 text-primary" />
                  Inventory Forecast
                </CardTitle>
              </CardHeader>
              <CardContent>
                {inventoryLoading ? (
                  <div className="flex items-center justify-center h-32">
                    <Loader2 className="h-8 w-8 animate-spin text-primary" />
                  </div>
                ) : inventoryData?.data && inventoryData.data.length > 0 ? (
                  <div className="space-y-3">
                    {inventoryData.data.slice(0, 5).map((item: any, index: number) => (
                      <div key={index} className="flex items-center justify-between rounded-lg border p-3">
                        <div>
                          <p className="font-medium">{item.product_name}</p>
                          <p className="text-xs text-muted-foreground">Stock: {item.current_stock}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-medium">{item.days_until_depletion} days</p>
                          <Badge variant={item.days_until_depletion < 7 ? 'destructive' : 'default'}>
                            {item.days_until_depletion < 7 ? 'Urgent' : 'Ok'}
                          </Badge>
                        </div>
                      </div>
                    ))}
                    <Button variant="link" className="w-full text-center" onClick={() => refetchInventory()}>
                      Refresh Data
                    </Button>
                  </div>
                ) : (
                  <div className="flex h-32 items-center justify-center text-muted-foreground">
                    No inventory forecast data
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Seasonality Detection */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="h-5 w-5 text-primary" />
                  Seasonality Detection
                </CardTitle>
              </CardHeader>
              <CardContent>
                {seasonalityLoading ? (
                  <div className="flex items-center justify-center h-32">
                    <Loader2 className="h-8 w-8 animate-spin text-primary" />
                  </div>
                ) : seasonalityData ? (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Seasonality Detected</span>
                      <Badge variant={seasonalityData.has_seasonality ? 'default' : 'secondary'}>
                        {seasonalityData.has_seasonality ? 'Yes' : 'No'}
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Seasonality Strength</span>
                      <span className="text-sm font-medium">
                        {(seasonalityData.seasonality_strength * 100).toFixed(1)}%
                      </span>
                    </div>
                    {seasonalityData.peak_days && seasonalityData.peak_days.length > 0 && (
                      <div>
                        <p className="text-sm text-muted-foreground">Peak Days</p>
                        <div className="flex flex-wrap gap-2 mt-1">
                          {seasonalityData.peak_days.map((day: string) => (
                            <Badge key={day} variant="default">{day}</Badge>
                          ))}
                        </div>
                      </div>
                    )}
                    <Button variant="link" className="w-full text-center" onClick={() => refetchSeasonality()}>
                      Refresh Data
                    </Button>
                  </div>
                ) : (
                  <div className="flex h-32 items-center justify-center text-muted-foreground">
                    No seasonality data available
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Moving Average */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5 text-primary" />
                Moving Average (7-day)
              </CardTitle>
            </CardHeader>
            <CardContent>
              {movingAverageLoading ? (
                <div className="flex items-center justify-center h-48">
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                </div>
              ) : movingAverageData?.data && movingAverageData.data.length > 0 ? (
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <RechartsLineChart data={movingAverageData.data}>
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
                      <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} dot={false} />
                      <Line type="monotone" dataKey="moving_avg" stroke="#f59e0b" strokeWidth={2} dot={false} strokeDasharray="5 5" />
                    </RechartsLineChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="flex h-48 items-center justify-center text-muted-foreground">
                  No moving average data available
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardContent className="p-6">
                <div className="text-center">
                  <Brain className="mx-auto h-8 w-8 text-primary mb-2" />
                  <p className="text-2xl font-bold">{demandForecast.length || 0}</p>
                  <p className="text-sm text-muted-foreground">Demand Points</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6">
                <div className="text-center">
                  <DollarSign className="mx-auto h-8 w-8 text-green-500 mb-2" />
                  <p className="text-2xl font-bold">
                    
                  </p>
                  <p className="text-sm text-muted-foreground">Total Revenue Forecast</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6">
                <div className="text-center">
                  <TrendingUp className="mx-auto h-8 w-8 text-blue-500 mb-2" />
                  <p className="text-2xl font-bold">
                    
                  </p>
                  <p className="text-sm text-muted-foreground">Total Profit Forecast</p>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-primary" />
                Prediction Summary
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between border-b pb-2">
                  <span className="text-sm font-medium">Model Used</span>
                  <Badge>{model}</Badge>
                </div>
                <div className="flex items-center justify-between border-b pb-2">
                  <span className="text-sm font-medium">Forecast Period</span>
                  <span className="text-sm">{days} days</span>
                </div>
                <div className="flex items-center justify-between border-b pb-2">
                  <span className="text-sm font-medium">Demand Points</span>
                  <span className="text-sm">{demandForecast.length}</span>
                </div>
                <div className="flex items-center justify-between border-b pb-2">
                  <span className="text-sm font-medium">Revenue Points</span>
                  <span className="text-sm">{revenueForecast.length}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Profit Points</span>
                  <span className="text-sm">{profitForecast.length}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </motion.div>
  );
};

