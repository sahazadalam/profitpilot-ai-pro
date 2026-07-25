import { ChartCard } from '@/components/shared/ChartCard';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

interface CategoryAnalyticsProps {
  data: {
    data: Array<{
      category: string;
      total_sale_amount: number;
      profit: number;
      quantity: number;
    }>;
  };
}

export const CategoryAnalytics = ({ data }: CategoryAnalyticsProps) => {
  const chartData = data?.data || [];
  const COLORS = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899'];

  const formatCurrency = (value: number) => {
    return '$' + value.toFixed(2);
  };

  return (
    <ChartCard title="Category Performance">
      <div className="h-64">
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => {
                  return name + ' ' + (percent * 100).toFixed(0) + '%';
                }}
                outerRadius={80}
                fill="#8884d8"
                dataKey="total_sale_amount"
              >
                {chartData.map((entry: any, index: number) => (
                  <Cell key={'cell-' + index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: 'var(--background)',
                  border: '1px solid var(--border)',
                  borderRadius: '8px',
                }}
                formatter={(value: number) => [formatCurrency(value), 'Revenue']}
              />
            </PieChart>
          </ResponsiveContainer>
        ) : (
          <div className="flex h-full items-center justify-center text-muted-foreground">
            No category data available
          </div>
        )}
      </div>
    </ChartCard>
  );
};

