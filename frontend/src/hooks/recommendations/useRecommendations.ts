import { useQuery } from '@tanstack/react-query';
import { recommendationsService } from '@/services/recommendations';

export const useRecommendations = () => {
  const restock = useQuery({
    queryKey: ['recommendations', 'restock'],
    queryFn: recommendationsService.getRestockRecommendations,
    staleTime: 5 * 60 * 1000,
  });

  const pricing = useQuery({
    queryKey: ['recommendations', 'pricing'],
    queryFn: recommendationsService.getPricingRecommendations,
    staleTime: 5 * 60 * 1000,
  });

  const deadStock = useQuery({
    queryKey: ['recommendations', 'dead-stock'],
    queryFn: recommendationsService.getDeadStock,
    staleTime: 5 * 60 * 1000,
  });

  const lossProducts = useQuery({
    queryKey: ['recommendations', 'loss-products'],
    queryFn: recommendationsService.getLossProducts,
    staleTime: 5 * 60 * 1000,
  });

  const bundles = useQuery({
    queryKey: ['recommendations', 'bundles'],
    queryFn: recommendationsService.getBundles,
    staleTime: 5 * 60 * 1000,
  });

  const performance = useQuery({
    queryKey: ['recommendations', 'performance'],
    queryFn: recommendationsService.getPerformanceScores,
    staleTime: 5 * 60 * 1000,
  });

  const risk = useQuery({
    queryKey: ['recommendations', 'risk'],
    queryFn: recommendationsService.getBusinessRisk,
    staleTime: 5 * 60 * 1000,
  });

  const optimizations = useQuery({
    queryKey: ['recommendations', 'optimizations'],
    queryFn: recommendationsService.getOptimizations,
    staleTime: 5 * 60 * 1000,
  });

  const executiveSummary = useQuery({
    queryKey: ['recommendations', 'executive'],
    queryFn: recommendationsService.getExecutiveSummary,
    staleTime: 5 * 60 * 1000,
  });

  return {
    restock,
    pricing,
    deadStock,
    lossProducts,
    bundles,
    performance,
    risk,
    optimizations,
    executiveSummary,
    isLoading: restock.isLoading || pricing.isLoading || risk.isLoading,
    error: restock.error || pricing.error || risk.error,
  };
};
