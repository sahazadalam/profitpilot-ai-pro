import { ChartCard } from '@/components/shared/ChartCard';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { RevenueAnalytics as RevenueType } from '@/types/analytics';

interface RevenueAnalyticsProps {
  data: RevenueType;
}

export const RevenueAnalytics = ({ data }: RevenueAnalyticsProps) => {
  const chartData = [
    { name: 'Today', value: data?.today || 0 },
    { name: 'Weekly', value: data?.weekly || 0 },
    { name: 'Monthly', value: data?.monthly || 0 },
    { name: 'Yearly', value: data?.yearly || 0 },
    { name: 'Total', value: data?.total || 0 },
  ];

  const formatCurrency = (value: number) => {
    return '$' + value.toLocaleString();
  };

  return (
    <ChartCard title="Revenue Analytics">
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis dataKey="name" className="text-xs" />
            <YAxis className="text-xs" />
            <Tooltip
              contentStyle={{
                background: 'var(--background)',
                border: '1px solid var(--border)',
                borderRadius: '8px',
              }}
              formatter={(value: number) => [formatCurrency(value), 'Revenue']}
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke="#3b82f6"
              strokeWidth={2}
              fill="url(#revenueGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
};

