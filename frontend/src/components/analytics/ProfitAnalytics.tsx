import { ChartCard } from '@/components/shared/ChartCard';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ProfitAnalytics as ProfitType } from '@/types/analytics';

interface ProfitAnalyticsProps {
  data: ProfitType;
}

export const ProfitAnalytics = ({ data }: ProfitAnalyticsProps) => {
  const chartData = [
    { name: 'Today', profit: data?.today || 0 },
    { name: 'Weekly', profit: data?.weekly || 0 },
    { name: 'Monthly', profit: data?.monthly || 0 },
    { name: 'Yearly', profit: data?.yearly || 0 },
    { name: 'Total', profit: data?.total || 0 },
  ];

  const formatCurrency = (value: number) => {
    return '$' + value.toLocaleString();
  };

  return (
    <ChartCard title="Profit Analytics">
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis dataKey="name" className="text-xs" />
            <YAxis className="text-xs" />
            <Tooltip
              contentStyle={{
                background: 'var(--background)',
                border: '1px solid var(--border)',
                borderRadius: '8px',
              }}
              formatter={(value: number) => [formatCurrency(value), 'Profit']}
            />
            <Bar dataKey="profit" fill="#10b981" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
};
