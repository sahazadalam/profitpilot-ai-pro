import { motion } from 'framer-motion';
import { useAnalytics } from '@/hooks/analytics/useAnalytics';
import { RevenueAnalytics } from '@/components/analytics/RevenueAnalytics';
import { ProfitAnalytics } from '@/components/analytics/ProfitAnalytics';
import { BusinessHealth } from '@/components/analytics/BusinessHealth';
import { KPIs } from '@/components/analytics/KPIs';
import { Insights } from '@/components/analytics/Insights';
import { TrendAnalysis } from '@/components/analytics/TrendAnalysis';
import { CategoryAnalytics } from '@/components/analytics/CategoryAnalytics';
import { LoadingSkeleton } from '@/components/shared/LoadingSkeleton';

export const AnalyticsDashboard = () => {
  const { revenue, profit, health, kpis, insights, trends, categories, isLoading } = useAnalytics();

  if (isLoading) {
    return <LoadingSkeleton />;
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6 p-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Analytics</h1>
          <p className="text-muted-foreground">Comprehensive business intelligence</p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <KPIs data={kpis.data} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <RevenueAnalytics data={revenue.data} />
        <ProfitAnalytics data={profit.data} />
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="md:col-span-2">
          <TrendAnalysis data={trends.data} />
        </div>
        <div>
          <BusinessHealth data={health.data} />
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <CategoryAnalytics data={categories.data} />
        <Insights data={insights.data} />
      </div>
    </motion.div>
  );
};
