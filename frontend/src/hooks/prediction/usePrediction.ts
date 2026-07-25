import { useQuery, useMutation } from '@tanstack/react-query';
import { predictionService } from '@/services/prediction';

export const usePrediction = () => {
  const demand = useMutation({
    mutationFn: predictionService.predictDemand,
  });

  const revenue = useMutation({
    mutationFn: predictionService.predictRevenue,
  });

  const profit = useMutation({
    mutationFn: predictionService.predictProfit,
  });

  const inventory = useQuery({
    queryKey: ['prediction', 'inventory'],
    queryFn: predictionService.getInventoryForecast,
    staleTime: 5 * 60 * 1000,
  });

  const seasonality = useQuery({
    queryKey: ['prediction', 'seasonality'],
    queryFn: predictionService.getSeasonality,
    staleTime: 5 * 60 * 1000,
  });

  const movingAverage = useQuery({
    queryKey: ['prediction', 'moving-average'],
    queryFn: () => predictionService.getMovingAverage(7),
    staleTime: 5 * 60 * 1000,
  });

  const models = useQuery({
    queryKey: ['prediction', 'models'],
    queryFn: predictionService.getModels,
    staleTime: 5 * 60 * 1000,
  });

  const compareModels = useMutation({
    mutationFn: predictionService.compareModels,
  });

  return {
    demand,
    revenue,
    profit,
    inventory,
    seasonality,
    movingAverage,
    models,
    compareModels,
  };
};
