import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { useRecommendations } from '@/hooks/recommendations/useRecommendations';
import { RestockRecommendations } from '@/components/recommendations/RestockRecommendations';
import { PricingRecommendations } from '@/components/recommendations/PricingRecommendations';
import { DeadStock } from '@/components/recommendations/DeadStock';
import { LossProducts } from '@/components/recommendations/LossProducts';
import { Bundles } from '@/components/recommendations/Bundles';
import { PerformanceAnalysis } from '@/components/recommendations/PerformanceAnalysis';
import { BusinessRisk } from '@/components/recommendations/BusinessRisk';
import { ExecutiveSummary } from '@/components/recommendations/ExecutiveSummary';
import { LoadingSkeleton } from '@/components/shared/LoadingSkeleton';

export const RecommendationsDashboard = () => {
  const { restock, pricing, deadStock, lossProducts, bundles, performance, risk, executiveSummary, isLoading } = useRecommendations();

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
          <h1 className="text-3xl font-bold tracking-tight">Recommendations</h1>
          <p className="text-muted-foreground">AI-powered business recommendations</p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <ExecutiveSummary data={executiveSummary.data} />
        <BusinessRisk data={risk.data} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <RestockRecommendations data={restock.data} />
        <PricingRecommendations data={pricing.data} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <DeadStock data={deadStock.data} />
        <LossProducts data={lossProducts.data} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Bundles data={bundles.data} />
        <PerformanceAnalysis data={performance.data} />
      </div>
    </motion.div>
  );
};

