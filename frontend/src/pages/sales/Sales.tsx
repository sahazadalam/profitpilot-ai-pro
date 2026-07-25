import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { 
  Plus, 
  Search, 
  Download,
  DollarSign,
  TrendingUp,
  ShoppingBag,
  Calendar,
  Trash2,
  RefreshCw,
  Eye,
  AlertCircle
} from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/Dialog';
import { Label } from '@/components/ui/Label';
import { useNavigate } from 'react-router-dom';
import { api } from '@/services/api';
import toast from 'react-hot-toast';

interface Sale {
  id: string;
  invoice_number: string;
  customer_name: string;
  product_name: string;
  quantity: number;
  amount: number;
  profit: number;
  payment_method: string;
  status: string;
  date: string;
  sale_date?: string;
  total_sale_amount?: number;
}

export const Sales = () => {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [saleToDelete, setSaleToDelete] = useState<Sale | null>(null);
  const [isLoadingSubmit, setIsLoadingSubmit] = useState(false);
  const [formData, setFormData] = useState({
    product_id: '',
    quantity: 1,
    customer_name: '',
    payment_method: 'cash',
    invoice_number: '',
  });

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['sales', search],
    queryFn: async () => {
      try {
        const response = await api.get('/sales', { params: { search } });
        return response.data;
      } catch (error) {
        return { data: [] };
      }
    },
  });

  const { data: productsData } = useQuery({
    queryKey: ['products-dropdown'],
    queryFn: async () => {
      try {
        const response = await api.get('/products', { params: { limit: 100 } });
        return response.data;
      } catch (error) {
        return { data: [] };
      }
    },
  });

  const createMutation = useMutation({
    mutationFn: async (data: any) => {
      const payload = {
        product_id: data.product_id,
        quantity: parseInt(data.quantity) || 1,
        customer_name: data.customer_name || '',
        payment_method: data.payment_method || 'cash',
        invoice_number: data.invoice_number,
      };
      const response = await api.post('/sales', payload);
      return response.data;
    },
    onSuccess: () => {
      toast.success('Sale created successfully!');
      setIsModalOpen(false);
      resetForm();
      refetch();
      setIsLoadingSubmit(false);
    },
    onError: (error: any) => {
      const errorMsg = error.response?.data?.message || 'Failed to create sale';
      toast.error(errorMsg);
      setIsLoadingSubmit(false);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      const response = await api.delete(/sales/);
      return response.data;
    },
    onSuccess: () => {
      toast.success('Sale deleted successfully!');
      setIsDeleteModalOpen(false);
      setSaleToDelete(null);
      refetch();
    },
    onError: (error: any) => {
      const errorMsg = error.response?.data?.message || 'Failed to delete sale';
      toast.error(errorMsg);
    },
  });

  const resetForm = () => {
    setFormData({
      product_id: '',
      quantity: 1,
      customer_name: '',
      payment_method: 'cash',
      invoice_number: '',
    });
  };

  const handleDelete = (sale: Sale) => {
    setSaleToDelete(sale);
    setIsDeleteModalOpen(true);
  };

  const confirmDelete = () => {
    if (saleToDelete) {
      deleteMutation.mutate(saleToDelete.id);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.product_id) {
      toast.error('Please select a product');
      return;
    }
    if (!formData.invoice_number.trim()) {
      toast.error('Invoice number is required');
      return;
    }
    if (formData.quantity < 1) {
      toast.error('Quantity must be at least 1');
      return;
    }

    setIsLoadingSubmit(true);
    createMutation.mutate(formData);
  };

  const sales = data?.data || [];
  const products = productsData?.data || [];

  const totalRevenue = sales.reduce((sum: number, s: any) => sum + (s.total_sale_amount || s.amount || 0), 0);
  const totalProfit = sales.reduce((sum: number, s: any) => sum + (s.profit || 0), 0);
  const totalSales = sales.length;
  
  const today = new Date().toDateString();
  const todaySales = sales.filter((s: any) => {
    const saleDate = new Date(s.sale_date || s.date).toDateString();
    return saleDate === today;
  }).length;

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount || 0);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-white">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6 bg-white">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-gray-900">Sales</h1>
            <p className="text-gray-500">Track and manage your sales transactions</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" className="gap-2" onClick={() => refetch()}>
              <RefreshCw className="h-4 w-4" />
              Refresh
            </Button>
            <Button size="sm" className="gap-2 bg-blue-600 hover:bg-blue-700 text-white" onClick={() => { resetForm(); setIsModalOpen(true); }}>
              <Plus className="h-4 w-4" />
              New Sale
            </Button>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card className="border-l-4 border-l-blue-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total Revenue</p>
                  <p className="text-2xl font-bold text-blue-600">{formatCurrency(totalRevenue)}</p>
                </div>
                <DollarSign className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>
          <Card className="border-l-4 border-l-green-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total Profit</p>
                  <p className="text-2xl font-bold text-green-600">{formatCurrency(totalProfit)}</p>
                </div>
                <TrendingUp className="h-8 w-8 text-green-500" />
              </div>
            </CardContent>
          </Card>
          <Card className="border-l-4 border-l-purple-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total Sales</p>
                  <p className="text-2xl font-bold text-purple-600">{totalSales}</p>
                </div>
                <ShoppingBag className="h-8 w-8 text-purple-500" />
              </div>
            </CardContent>
          </Card>
          <Card className="border-l-4 border-l-orange-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Today's Sales</p>
                  <p className="text-2xl font-bold text-orange-600">{todaySales}</p>
                </div>
                <Calendar className="h-8 w-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Search */}
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Search sales by invoice, customer, or product..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* Sales Table */}
        <Card>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Invoice</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Qty</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {sales.length === 0 ? (
                    <tr>
                      <td colSpan={8} className="px-6 py-12 text-center text-gray-500">
                        <ShoppingBag className="h-12 w-12 mx-auto text-gray-300 mb-4" />
                        <p className="text-lg font-medium">No sales found</p>
                        <p className="text-sm">Click "New Sale" to create one.</p>
                      </td>
                    </tr>
                  ) : (
                    sales.map((sale: any) => (
                      <motion.tr 
                        key={sale.id} 
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3 }}
                        className="hover:bg-gray-50"
                      >
                        <td className="px-6 py-4 font-medium text-gray-900">{sale.invoice_number}</td>
                        <td className="px-6 py-4 text-gray-700">{sale.product_name}</td>
                        <td className="px-6 py-4 text-gray-700">{sale.customer_name || 'N/A'}</td>
                        <td className="px-6 py-4 text-gray-700">{sale.quantity}</td>
                        <td className="px-6 py-4">
                          <p className="font-medium text-gray-900">{formatCurrency(sale.total_sale_amount || sale.amount || 0)}</p>
                          <p className="text-xs text-green-600">Profit: {formatCurrency(sale.profit || 0)}</p>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500">
                          {new Date(sale.sale_date || sale.date).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Completed
                          </span>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <div className="flex justify-end gap-2">
                            <Button 
                              variant="ghost" 
                              size="sm" 
                              onClick={() => navigate(/sales/)}
                              className="text-blue-600 hover:text-blue-700"
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm" 
                              onClick={() => handleDelete(sale)} 
                              className="text-red-500 hover:text-red-700"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </td>
                      </motion.tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between text-sm text-gray-500 border-t border-gray-200 pt-6">
          <span>© 2026 ProfitPilot AI Pro. All rights reserved.</span>
          <span className="flex items-center gap-2 mt-2 sm:mt-0">
            Built with React 19 · TypeScript · AI-Powered
            <span className="inline-block w-2 h-2 bg-blue-600 rounded-full animate-pulse"></span>
          </span>
        </div>
      </div>
    </div>
  );
};

export default Sales;

