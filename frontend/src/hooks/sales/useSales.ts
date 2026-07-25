import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { salesApi } from '@/services/sales/salesApi';
import toast from 'react-hot-toast';

export const useSales = (search?: string) => {
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery({
    queryKey: ['sales', search],
    queryFn: () => salesApi.getSales({ search }),
    staleTime: 5 * 60 * 1000,
  });

  const createSale = useMutation({
    mutationFn: salesApi.createSale,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      toast.success('Sale created successfully');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Failed to create sale');
    },
  });

  const deleteSale = useMutation({
    mutationFn: salesApi.deleteSale,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      toast.success('Sale deleted successfully');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Failed to delete sale');
    },
  });

  return {
    data: data?.data || data,
    isLoading,
    error,
    createSale: createSale.mutateAsync,
    deleteSale: deleteSale.mutateAsync,
  };
};

