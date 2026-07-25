import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { 
  Plus, 
  Search, 
  Edit, 
  Trash2, 
  Package, 
  AlertCircle, 
  RefreshCw,
  Eye,
  Filter
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

interface Product {
  id: string;
  name: string;
  description?: string;
  category: string;
  sku: string;
  supplier?: string;
  purchase_price: number;
  selling_price: number;
  stock: number;
  minimum_stock: number;
  status: string;
}

export const Inventory = () => {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [productToDelete, setProductToDelete] = useState<Product | null>(null);
  const [isLoadingSubmit, setIsLoadingSubmit] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: '',
    sku: '',
    supplier: '',
    purchase_price: 0,
    selling_price: 0,
    stock: 0,
    minimum_stock: 5,
    status: 'active',
  });

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['products', search],
    queryFn: async () => {
      try {
        const response = await api.get('/products', { params: { search } });
        return response.data;
      } catch (error) {
        return { data: [] };
      }
    },
  });

  const { data: summary, refetch: refetchSummary } = useQuery({
    queryKey: ['products-summary'],
    queryFn: async () => {
      try {
        const response = await api.get('/products/summary');
        return response.data.data || {};
      } catch (error) {
        return {};
      }
    },
  });

  const createMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/products', data);
      return response.data;
    },
    onSuccess: () => {
      toast.success('Product created successfully!');
      setIsModalOpen(false);
      resetForm();
      refetch();
      refetchSummary();
      setIsLoadingSubmit(false);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Failed to create product');
      setIsLoadingSubmit(false);
    },
  });

  const updateMutation = useMutation({
    mutationFn: async ({ id, data }: { id: string; data: any }) => {
      const response = await api.put(/products/, data);
      return response.data;
    },
    onSuccess: () => {
      toast.success('Product updated successfully!');
      setIsModalOpen(false);
      setSelectedProduct(null);
      resetForm();
      refetch();
      refetchSummary();
      setIsLoadingSubmit(false);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Failed to update product');
      setIsLoadingSubmit(false);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      const response = await api.delete(/products/);
      return response.data;
    },
    onSuccess: () => {
      toast.success('Product deleted successfully!');
      setIsDeleteModalOpen(false);
      setProductToDelete(null);
      refetch();
      refetchSummary();
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.message || 'Failed to delete product');
    },
  });

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      category: '',
      sku: '',
      supplier: '',
      purchase_price: 0,
      selling_price: 0,
      stock: 0,
      minimum_stock: 5,
      status: 'active',
    });
  };

  const handleEdit = (product: Product) => {
    setSelectedProduct(product);
    setFormData({
      name: product.name || '',
      description: product.description || '',
      category: product.category || '',
      sku: product.sku || '',
      supplier: product.supplier || '',
      purchase_price: product.purchase_price || 0,
      selling_price: product.selling_price || 0,
      stock: product.stock || 0,
      minimum_stock: product.minimum_stock || 5,
      status: product.status || 'active',
    });
    setIsModalOpen(true);
  };

  const handleDelete = (product: Product) => {
    setProductToDelete(product);
    setIsDeleteModalOpen(true);
  };

  const confirmDelete = () => {
    if (productToDelete) {
      deleteMutation.mutate(productToDelete.id);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoadingSubmit(true);
    
    if (!formData.name.trim()) {
      toast.error('Product name is required');
      setIsLoadingSubmit(false);
      return;
    }

    if (selectedProduct) {
      updateMutation.mutate({ id: selectedProduct.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const products = data?.data || [];
  const summaryData = summary || {};

  const getStatusBadge = (status: string) => {
    const variants: Record<string, string> = {
      'active': 'bg-green-100 text-green-800',
      'inactive': 'bg-gray-100 text-gray-800',
      'discontinued': 'bg-red-100 text-red-800'
    };
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

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
      <div className="flex items-center justify-center h-64" style={{ backgroundColor: '#f1f5f9' }}>
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div style={{ backgroundColor: '#f1f5f9', minHeight: '100vh', padding: '24px' }}>
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-gray-900">Inventory</h1>
            <p className="text-gray-500">Manage your products and stock levels</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" className="gap-2" onClick={() => refetch()}>
              <RefreshCw className="h-4 w-4" />
              Refresh
            </Button>
            <Button size="sm" className="gap-2 bg-blue-600 hover:bg-blue-700 text-white" onClick={() => { resetForm(); setSelectedProduct(null); setIsModalOpen(true); }}>
              <Plus className="h-4 w-4" />
              Add Product
            </Button>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card className="border-l-4 border-l-blue-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total Products</p>
                  <p className="text-2xl font-bold text-gray-900">{summaryData.total_products || 0}</p>
                </div>
                <Package className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>
          <Card className="border-l-4 border-l-green-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total Stock</p>
                  <p className="text-2xl font-bold text-gray-900">{summaryData.total_stock || 0}</p>
                </div>
                <Package className="h-8 w-8 text-green-500" />
              </div>
            </CardContent>
          </Card>
          <Card className="border-l-4 border-l-yellow-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Low Stock</p>
                  <p className="text-2xl font-bold text-yellow-600">{summaryData.low_stock || 0}</p>
                </div>
                <AlertCircle className="h-8 w-8 text-yellow-500" />
              </div>
            </CardContent>
          </Card>
          <Card className="border-l-4 border-l-red-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Out of Stock</p>
                  <p className="text-2xl font-bold text-red-600">{summaryData.out_of_stock || 0}</p>
                </div>
                <AlertCircle className="h-8 w-8 text-red-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Search */}
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Search products..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10"
            />
          </div>
          <Button variant="outline" className="gap-2">
            <Filter className="h-4 w-4" />
            More Filters
          </Button>
        </div>

        {/* Products Table */}
        <Card>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {products.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                        No products found. Click "Add Product" to create one.
                      </td>
                    </tr>
                  ) : (
                    products.map((product: any) => (
                      <tr key={product.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4">
                          <div>
                            <p className="font-medium text-gray-900">{product.name}</p>
                            <p className="text-xs text-gray-500">SKU: {product.sku}</p>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <Badge variant="secondary">{product.category}</Badge>
                        </td>
                        <td className="px-6 py-4">
                          <div>
                            <p className="font-medium text-gray-900">{formatCurrency(product.selling_price)}</p>
                            <p className="text-xs text-gray-500">Cost: {formatCurrency(product.purchase_price)}</p>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div>
                            <p className={product.stock <= product.minimum_stock ? 'text-yellow-600 font-medium' : 'text-gray-900'}>
                              {product.stock}
                            </p>
                            <p className="text-xs text-gray-500">Min: {product.minimum_stock}</p>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          {getStatusBadge(product.status)}
                        </td>
                        <td className="px-6 py-4 text-right">
                          <div className="flex justify-end gap-2">
                            <Button variant="ghost" size="sm" onClick={() => navigate(/inventory/)}>
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm" onClick={() => handleEdit(product)}>
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm" onClick={() => handleDelete(product)} className="text-red-500 hover:text-red-700">
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </td>
                      </tr>
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

export default Inventory;

