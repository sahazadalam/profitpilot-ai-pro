import { useQuery } from '@tanstack/react-query';
import { analyticsService } from '@/services/analytics';

export const useAnalytics = () => {
  const revenue = useQuery({
    queryKey: ['analytics', 'revenue'],
    queryFn: analyticsService.getRevenue,
    staleTime: 5 * 60 * 1000,
  });

  const profit = useQuery({
    queryKey: ['analytics', 'profit'],
    queryFn: analyticsService.getProfit,
    staleTime: 5 * 60 * 1000,
  });

  const health = useQuery({
    queryKey: ['analytics', 'health'],
    queryFn: analyticsService.getBusinessHealth,
    staleTime: 5 * 60 * 1000,
  });

  const kpis = useQuery({
    queryKey: ['analytics', 'kpis'],
    queryFn: analyticsService.getKPIs,
    staleTime: 5 * 60 * 1000,
  });

  const insights = useQuery({
    queryKey: ['analytics', 'insights'],
    queryFn: analyticsService.getInsights,
    staleTime: 5 * 60 * 1000,
  });

  const trends = useQuery({
    queryKey: ['analytics', 'trends'],
    queryFn: analyticsService.getTrends,
    staleTime: 5 * 60 * 1000,
  });

  const categories = useQuery({
    queryKey: ['analytics', 'categories'],
    queryFn: analyticsService.getCategories,
    staleTime: 5 * 60 * 1000,
  });

  return {
    revenue,
    profit,
    health,
    kpis,
    insights,
    trends,
    categories,
    isLoading: revenue.isLoading || profit.isLoading || health.isLoading,
    error: revenue.error || profit.error || health.error,
  };
};
