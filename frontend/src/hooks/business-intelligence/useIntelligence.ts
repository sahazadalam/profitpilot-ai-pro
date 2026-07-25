import { useQuery, useMutation } from '@tanstack/react-query';
import { intelligenceService } from '@/services/business-intelligence';

export const useIntelligence = () => {
  const customerSegments = useQuery({
    queryKey: ['intelligence', 'segments'],
    queryFn: intelligenceService.getCustomerSegments,
    staleTime: 5 * 60 * 1000,
  });

  const anomalies = useQuery({
    queryKey: ['intelligence', 'anomalies'],
    queryFn: intelligenceService.getAnomalies,
    staleTime: 5 * 60 * 1000,
  });

  const marketTrends = useQuery({
    queryKey: ['intelligence', 'market-trends'],
    queryFn: intelligenceService.getMarketTrends,
    staleTime: 5 * 60 * 1000,
  });

  const riskPrediction = useQuery({
    queryKey: ['intelligence', 'risk'],
    queryFn: intelligenceService.getRiskPrediction,
    staleTime: 5 * 60 * 1000,
  });

  const insights = useQuery({
    queryKey: ['intelligence', 'insights'],
    queryFn: intelligenceService.getAIInsights,
    staleTime: 5 * 60 * 1000,
  });

  const explainableAI = useQuery({
    queryKey: ['intelligence', 'explain'],
    queryFn: intelligenceService.getExplainableAI,
    staleTime: 5 * 60 * 1000,
  });

  const simulate = useMutation({
    mutationFn: intelligenceService.simulateScenario,
  });

  const compareScenarios = useMutation({
    mutationFn: ({ scenarioA, scenarioB }: any) =>
      intelligenceService.compareScenarios(scenarioA, scenarioB),
  });

  return {
    customerSegments,
    anomalies,
    marketTrends,
    riskPrediction,
    insights,
    explainableAI,
    simulate,
    compareScenarios,
    isLoading: customerSegments.isLoading || anomalies.isLoading || riskPrediction.isLoading,
    error: customerSegments.error || anomalies.error || riskPrediction.error,
  };
};

