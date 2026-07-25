import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { 
  Plus, Search, Download, DollarSign, ShoppingCart, Calendar, 
  TrendingUp, Trash2, Printer, AlertCircle, RefreshCw 
} from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/Dialog';
import { Label } from '@/components/ui/Label';
import { api } from '@/services/api';
import toast from 'react-hot-toast';
import * as XLSX from 'xlsx';

export const Sales = () => {
  const [search, setSearch] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [saleToDelete, setSaleToDelete] = useState(null);
  const [isLoadingSubmit, setIsLoadingSubmit] = useState(false);
  const [formData, setFormData] = useState({
    product_id: '',
    quantity: 1,
    customer_name: '',
    payment_method: 'cash',
    invoice_number: '',
  });
  const [products, setProducts] = useState([]);
  const queryClient = useQueryClient();

  // Fetch sales
  const { data, isLoading, refetch } = useQuery({
    queryKey: ['sales', search],
    queryFn: async () => {
      try {
        const response = await api.get('/sales', { params: { search } });
        console.log('Sales data:', response.data);
        return response.data;
      } catch (error) {
        console.error('Error fetching sales:', error);
        return { data: [] };
      }
    },
  });

  // Fetch products for dropdown
  const { data: productsData } = useQuery({
    queryKey: ['products-dropdown'],
    queryFn: async () => {
      try {
        const response = await api.get('/products', { params: { limit: 100 } });
        setProducts(response.data.data || []);
        return response.data;
      } catch (error) {
        console.error('Error fetching products:', error);
        return { data: [] };
      }
    },
  });

  // Fetch analytics from dashboard
  const { data: analytics, refetch: refetchAnalytics } = useQuery({
    queryKey: ['sales-analytics'],
    queryFn: async () => {
      try {
        const response = await api.get('/dashboard');
        console.log('Analytics data from dashboard:', response.data);
        return response.data.data || {};
      } catch (error) {
        console.error('Error fetching analytics:', error);
        return {};
      }
    },
  });

  // Create sale mutation
  const createMutation = useMutation({
    mutationFn: async (data) => {
      const payload = {
        product_id: data.product_id,
        quantity: parseInt(data.quantity) || 1,
        customer_name: data.customer_name || '',
        payment_method: data.payment_method || 'cash',
        invoice_number: data.invoice_number,
      };
      console.log('Creating sale with payload:', payload);
      const response = await api.post('/sales', payload);
      return response.data;
    },
    onSuccess: () => {
      toast.success('Sale created successfully!');
      setIsModalOpen(false);
      resetForm();
      refetch();
      refetchAnalytics();
      setIsLoadingSubmit(false);
    },
    onError: (error) => {
      console.error('Create sale error:', error);
      const errorMsg = error.response?.data?.error?.message || error.response?.data?.message || 'Failed to create sale';
      toast.error(errorMsg);
      setIsLoadingSubmit(false);
    },
  });

  // Delete sale mutation
  const deleteMutation = useMutation({
    mutationFn: async (id) => {
      console.log('Deleting sale with ID:', id);
      const response = await api.delete(/sales/);
      return response.data;
    },
    onSuccess: () => {
      toast.success('Sale deleted successfully!');
      setIsDeleteModalOpen(false);
      setSaleToDelete(null);
      refetch();
      refetchAnalytics();
    },
    onError: (error) => {
      console.error('Delete sale error:', error);
      const errorMsg = error.response?.data?.error?.message || error.response?.data?.message || 'Failed to delete sale';
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

  const handleDelete = (sale) => {
    setSaleToDelete(sale);
    setIsDeleteModalOpen(true);
  };

  const confirmDelete = () => {
    if (saleToDelete) {
      deleteMutation.mutate(saleToDelete.id);
    }
  };

  const handleSubmit = (e) => {
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

  const handleExportCSV = () => {
    try {
      const salesData = data?.data || [];
      if (salesData.length === 0) {
        toast.error('No data to export');
        return;
      }

      const exportData = salesData.map(sale => ({
        'Invoice Number': sale.invoice_number,
        'Product': sale.product_name,
        'Customer': sale.customer_name || 'N/A',
        'Quantity': sale.quantity,
        'Amount': sale.total_sale_amount,
        'Date': new Date(sale.sale_date).toLocaleDateString(),
        'Status': 'Completed'
      }));

      const ws = XLSX.utils.json_to_sheet(exportData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Sales');
      XLSX.writeFile(wb, sales_export_.xlsx);
      toast.success('Sales exported successfully!');
    } catch (error) {
      console.error('Export error:', error);
      toast.error('Failed to export sales');
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const handleRefresh = () => {
    refetch();
    refetchAnalytics();
    toast.success('Data refreshed');
  };

  const sales = data?.data || [];
  const analyticsData = analytics || {};
  
  // Calculate totals from sales data if analytics not available
  let totalRevenue = 0;
  let totalProfit = 0;
  let totalSales = sales.length;
  let todaySales = 0;

  // If analytics data is available, use it
  if (analyticsData.revenue !== undefined && analyticsData.revenue !== null) {
    totalRevenue = analyticsData.revenue;
    totalProfit = analyticsData.profit || 0;
    totalSales = analyticsData.total_sales || sales.length;
    todaySales = analyticsData.today_sales || 0;
  } else {
    // Calculate from sales data
    sales.forEach(sale => {
      totalRevenue += sale.total_sale_amount || 0;
      totalProfit += sale.profit || 0;
    });
    
    // Calculate today's sales
    const today = new Date().toDateString();
    todaySales = sales.filter(sale => {
      const saleDate = new Date(sale.sale_date).toDateString();
      return saleDate === today;
    }).length;
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Sales</h1>
          <p className="text-muted-foreground">Track and manage your sales transactions</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" size="sm" className="gap-2" onClick={handleRefresh}>
            <RefreshCw className="h-4 w-4" />
            Refresh
          </Button>
          <Button variant="outline" size="sm" className="gap-2" onClick={handleExportCSV}>
            <Download className="h-4 w-4" />
            Export
          </Button>
          <Button variant="outline" size="sm" className="gap-2" onClick={handlePrint}>
            <Printer className="h-4 w-4" />
            Print
          </Button>
          <Button size="sm" onClick={() => { resetForm(); setIsModalOpen(true); }} className="gap-2">
            <Plus className="h-4 w-4" />
            New Sale
          </Button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Revenue</p>
                <p className="text-2xl font-bold"></p>
              </div>
              <DollarSign className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Profit</p>
                <p className="text-2xl font-bold"></p>
              </div>
              <TrendingUp className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Sales</p>
                <p className="text-2xl font-bold">{totalSales}</p>
              </div>
              <ShoppingCart className="h-8 w-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Today's Sales</p>
                <p className="text-2xl font-bold">{todaySales}</p>
              </div>
              <Calendar className="h-8 w-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardContent className="p-6">
          <div className="mb-4 flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search sales..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-9"
              />
            </div>
          </div>

          <div className="relative overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="px-4 py-3 text-left">Invoice</th>
                  <th className="px-4 py-3 text-left">Product</th>
                  <th className="px-4 py-3 text-left">Customer</th>
                  <th className="px-4 py-3 text-left">Qty</th>
                  <th className="px-4 py-3 text-left">Amount</th>
                  <th className="px-4 py-3 text-left">Date</th>
                  <th className="px-4 py-3 text-left">Status</th>
                  <th className="px-4 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {sales.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="px-4 py-8 text-center text-muted-foreground">
                      No sales found. Click "New Sale" to create one.
                    </td>
                  </tr>
                ) : (
                  sales.map((sale, index) => (
                    <motion.tr
                      key={sale.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                      className="border-b hover:bg-muted/50"
                    >
                      <td className="px-4 py-3 font-medium">{sale.invoice_number}</td>
                      <td className="px-4 py-3">{sale.product_name}</td>
                      <td className="px-4 py-3">{sale.customer_name || 'N/A'}</td>
                      <td className="px-4 py-3">{sale.quantity}</td>
                      <td className="px-4 py-3 font-medium"></td>
                      <td className="px-4 py-3 text-muted-foreground">
                        {new Date(sale.sale_date).toLocaleDateString()}
                      </td>
                      <td className="px-4 py-3">
                        <Badge variant="success">Completed</Badge>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          onClick={() => handleDelete(sale)}
                          className="text-red-500 hover:text-red-700"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </td>
                    </motion.tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Create Sale Modal */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>New Sale</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit}>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label>Product *</Label>
                <select
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  value={formData.product_id}
                  onChange={(e) => setFormData({ ...formData, product_id: e.target.value })}
                  required
                >
                  <option value="">Select a product...</option>
                  {products.map((product) => (
                    <option key={product.id} value={product.id}>
                      {product.name} -  (Stock: {product.stock})
                    </option>
                  ))}
                </select>
              </div>
              <div className="space-y-2">
                <Label>Quantity *</Label>
                <Input
                  type="number"
                  min="1"
                  value={formData.quantity}
                  onChange={(e) => setFormData({ ...formData, quantity: parseInt(e.target.value) || 1 })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label>Customer Name</Label>
                <Input
                  value={formData.customer_name}
                  onChange={(e) => setFormData({ ...formData, customer_name: e.target.value })}
                  placeholder="Walk-in Customer"
                />
              </div>
              <div className="space-y-2">
                <Label>Payment Method</Label>
                <select
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  value={formData.payment_method}
                  onChange={(e) => setFormData({ ...formData, payment_method: e.target.value })}
                >
                  <option value="cash">Cash</option>
                  <option value="card">Card</option>
                  <option value="online">Online</option>
                  <option value="credit">Credit</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label>Invoice Number *</Label>
                <Input
                  value={formData.invoice_number}
                  onChange={(e) => setFormData({ ...formData, invoice_number: e.target.value })}
                  placeholder="INV-001"
                  required
                />
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => { setIsModalOpen(false); resetForm(); }}>
                Cancel
              </Button>
              <Button type="submit" disabled={isLoadingSubmit}>
                {isLoadingSubmit ? 'Creating...' : 'Create Sale'}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Modal */}
      <Dialog open={isDeleteModalOpen} onOpenChange={setIsDeleteModalOpen}>
        <DialogContent className="sm:max-w-[400px]">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-red-600">
              <AlertCircle className="h-5 w-5" />
              Confirm Delete
            </DialogTitle>
          </DialogHeader>
          <div className="py-4">
            <p className="text-sm text-muted-foreground">
              Are you sure you want to delete this sale?
              This action cannot be undone.
            </p>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => { setIsDeleteModalOpen(false); setSaleToDelete(null); }}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={confirmDelete} disabled={deleteMutation.isPending}>
              {deleteMutation.isPending ? 'Deleting...' : 'Delete Sale'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

