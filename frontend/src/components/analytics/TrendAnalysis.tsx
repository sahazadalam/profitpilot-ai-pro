import { ChartCard } from '@/components/shared/ChartCard';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface TrendAnalysisProps {
  data: {
    daily: {
      dates: string[];
      revenue: number[];
      profit: number[];
    };
  };
}

export const TrendAnalysis = ({ data }: TrendAnalysisProps) => {
  const dailyData = data?.daily || { dates: [], revenue: [], profit: [] };
  const chartData = dailyData.dates.map((date: string, i: number) => ({
    date: date,
    revenue: dailyData.revenue[i] || 0,
    profit: dailyData.profit[i] || 0,
  }));

  const formatCurrency = (value: number) => {
    return '$' + value.toLocaleString();
  };

  return (
    <ChartCard title="Revenue & Profit Trends">
      <div className="h-64">
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="trendRevenue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="trendProfit" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis dataKey="date" className="text-xs" />
              <YAxis className="text-xs" />
              <Tooltip
                contentStyle={{
                  background: 'var(--background)',
                  border: '1px solid var(--border)',
                  borderRadius: '8px',
                }}
                formatter={(value: number) => [formatCurrency(value), '']}
              />
              <Area
                type="monotone"
                dataKey="revenue"
                stroke="#3b82f6"
                strokeWidth={2}
                fill="url(#trendRevenue)"
              />
              <Area
                type="monotone"
                dataKey="profit"
                stroke="#10b981"
                strokeWidth={2}
                fill="url(#trendProfit)"
              />
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <div className="flex h-full items-center justify-center text-muted-foreground">
            No trend data available
          </div>
        )}
      </div>
    </ChartCard>
  );
};
