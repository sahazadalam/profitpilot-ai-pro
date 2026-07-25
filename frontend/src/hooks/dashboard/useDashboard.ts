import { useQuery } from '@tanstack/react-query';
import { dashboardApi } from '@/services/dashboard/dashboardApi';

export const useDashboard = () => {
  return useQuery({
    queryKey: ['dashboard'],
    queryFn: dashboardApi.getDashboard,
    staleTime: 5 * 60 * 1000,
  });
};
