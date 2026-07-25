import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { Plus, Search, Edit, Trash2, Package, AlertCircle, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/Dialog';
import { Label } from '@/components/ui/Label';
import { api } from '@/services/api';
import toast from 'react-hot-toast';

export const Inventory = () => {
  const [search, setSearch] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [productToDelete, setProductToDelete] = useState(null);
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
  const queryClient = useQueryClient();

  // Fetch products
  const { data, isLoading, refetch } = useQuery({
    queryKey: ['products', search],
    queryFn: async () => {
      try {
        const response = await api.get('/products', { params: { search } });
        console.log('Products data:', response.data);
        return response.data;
      } catch (error) {
        console.error('Error fetching products:', error);
        return { data: [] };
      }
    },
  });

  // Fetch summary
  const { data: summary, refetch: refetchSummary } = useQuery({
    queryKey: ['products-summary'],
    queryFn: async () => {
      try {
        const response = await api.get('/products/summary');
        console.log('Summary data:', response.data);
        return response.data.data || {};
      } catch (error) {
        console.error('Error fetching summary:', error);
        return {};
      }
    },
  });

  // Create product mutation
  const createMutation = useMutation({
    mutationFn: async (data) => {
      const payload = {
        name: data.name,
        description: data.description || '',
        category: data.category,
        sku: data.sku,
        supplier: data.supplier || '',
        purchase_price: parseFloat(data.purchase_price) || 0,
        selling_price: parseFloat(data.selling_price) || 0,
        stock: parseInt(data.stock) || 0,
        minimum_stock: parseInt(data.minimum_stock) || 5,
        status: data.status || 'active',
      };
      console.log('Creating product with payload:', payload);
      const response = await api.post('/products', payload);
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
    onError: (error) => {
      console.error('Create product error:', error);
      const errorMsg = error.response?.data?.error?.message || error.response?.data?.message || 'Failed to create product';
      toast.error(errorMsg);
      setIsLoadingSubmit(false);
    },
  });

  // Update product mutation
  const updateMutation = useMutation({
    mutationFn: async ({ id, data }) => {
      const payload = {
        name: data.name,
        description: data.description || '',
        category: data.category,
        sku: data.sku,
        supplier: data.supplier || '',
        purchase_price: parseFloat(data.purchase_price) || 0,
        selling_price: parseFloat(data.selling_price) || 0,
        stock: parseInt(data.stock) || 0,
        minimum_stock: parseInt(data.minimum_stock) || 5,
        status: data.status || 'active',
      };
      console.log('Updating product with payload:', payload);
      const response = await api.put(/products/, payload);
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
    onError: (error) => {
      console.error('Update product error:', error);
      const errorMsg = error.response?.data?.error?.message || error.response?.data?.message || 'Failed to update product';
      toast.error(errorMsg);
      setIsLoadingSubmit(false);
    },
  });

  // Delete product mutation
  const deleteMutation = useMutation({
    mutationFn: async (id) => {
      console.log('Deleting product with ID:', id);
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
    onError: (error) => {
      console.error('Delete product error:', error);
      const errorMsg = error.response?.data?.error?.message || error.response?.data?.message || 'Failed to delete product';
      toast.error(errorMsg);
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

  const handleEdit = (product) => {
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

  const handleDelete = (product) => {
    setProductToDelete(product);
    setIsDeleteModalOpen(true);
  };

  const confirmDelete = () => {
    if (productToDelete) {
      deleteMutation.mutate(productToDelete.id);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsLoadingSubmit(true);
    
    if (!formData.name.trim()) {
      toast.error('Product name is required');
      setIsLoadingSubmit(false);
      return;
    }
    if (!formData.category.trim()) {
      toast.error('Category is required');
      setIsLoadingSubmit(false);
      return;
    }
    if (!formData.sku.trim()) {
      toast.error('SKU is required');
      setIsLoadingSubmit(false);
      return;
    }
    if (formData.selling_price <= 0) {
      toast.error('Selling price must be greater than 0');
      setIsLoadingSubmit(false);
      return;
    }

    if (selectedProduct) {
      updateMutation.mutate({ id: selectedProduct.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleRefresh = () => {
    refetch();
    refetchSummary();
    toast.success('Data refreshed');
  };

  const products = data?.data || [];
  const summaryData = summary || {};

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
          <h1 className="text-3xl font-bold tracking-tight">Inventory</h1>
          <p className="text-muted-foreground">Manage your products and stock levels</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" size="sm" className="gap-2" onClick={handleRefresh}>
            <RefreshCw className="h-4 w-4" />
            Refresh
          </Button>
          <Button size="sm" onClick={() => { resetForm(); setSelectedProduct(null); setIsModalOpen(true); }} className="gap-2">
            <Plus className="h-4 w-4" />
            Add Product
          </Button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Products</p>
                <p className="text-2xl font-bold">{summaryData.total_products || 0}</p>
              </div>
              <Package className="h-8 w-8 text-muted-foreground" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Stock</p>
                <p className="text-2xl font-bold">{summaryData.total_stock || 0}</p>
              </div>
              <Package className="h-8 w-8 text-muted-foreground" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Low Stock</p>
                <p className="text-2xl font-bold text-yellow-500">{summaryData.low_stock || 0}</p>
              </div>
              <AlertCircle className="h-8 w-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Out of Stock</p>
                <p className="text-2xl font-bold text-red-500">{summaryData.out_of_stock || 0}</p>
              </div>
              <AlertCircle className="h-8 w-8 text-red-500" />
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
                placeholder="Search products..."
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
                  <th className="px-4 py-3 text-left">Product</th>
                  <th className="px-4 py-3 text-left">Category</th>
                  <th className="px-4 py-3 text-left">Price</th>
                  <th className="px-4 py-3 text-left">Stock</th>
                  <th className="px-4 py-3 text-left">Status</th>
                  <th className="px-4 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {products.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-4 py-8 text-center text-muted-foreground">
                      No products found. Click "Add Product" to create one.
                    </td>
                  </tr>
                ) : (
                  products.map((product, index) => (
                    <motion.tr
                      key={product.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                      className="border-b hover:bg-muted/50"
                    >
                      <td className="px-4 py-3">
                        <div>
                          <p className="font-medium">{product.name}</p>
                          <p className="text-xs text-muted-foreground">{product.sku}</p>
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <Badge variant="secondary">{product.category}</Badge>
                      </td>
                      <td className="px-4 py-3"></td>
                      <td className="px-4 py-3">
                        <span className={product.stock <= product.minimum_stock ? 'text-yellow-500' : ''}>
                          {product.stock}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <Badge variant={product.status === 'active' ? 'default' : 'secondary'}>
                          {product.status}
                        </Badge>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <div className="flex justify-end gap-2">
                          <Button variant="ghost" size="icon" onClick={() => handleEdit(product)}>
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="icon" onClick={() => handleDelete(product)} className="text-red-500 hover:text-red-700">
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

      {/* Add/Edit Product Modal */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{selectedProduct ? 'Edit Product' : 'Add New Product'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit}>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label>Product Name *</Label>
                <Input
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Enter product name"
                  required
                />
              </div>
              <div className="space-y-2">
                <Label>Description</Label>
                <Input
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Product description"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Category *</Label>
                  <Input
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    placeholder="Category"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label>SKU *</Label>
                  <Input
                    value={formData.sku}
                    onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
                    placeholder="SKU"
                    required
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label>Supplier</Label>
                <Input
                  value={formData.supplier}
                  onChange={(e) => setFormData({ ...formData, supplier: e.target.value })}
                  placeholder="Supplier name"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Purchase Price</Label>
                  <Input
                    type="number"
                    step="0.01"
                    value={formData.purchase_price}
                    onChange={(e) => setFormData({ ...formData, purchase_price: parseFloat(e.target.value) || 0 })}
                    placeholder="0.00"
                  />
                </div>
                <div className="space-y-2">
                  <Label>Selling Price *</Label>
                  <Input
                    type="number"
                    step="0.01"
                    value={formData.selling_price}
                    onChange={(e) => setFormData({ ...formData, selling_price: parseFloat(e.target.value) || 0 })}
                    placeholder="0.00"
                    required
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Stock</Label>
                  <Input
                    type="number"
                    value={formData.stock}
                    onChange={(e) => setFormData({ ...formData, stock: parseInt(e.target.value) || 0 })}
                    placeholder="0"
                  />
                </div>
                <div className="space-y-2">
                  <Label>Minimum Stock</Label>
                  <Input
                    type="number"
                    value={formData.minimum_stock}
                    onChange={(e) => setFormData({ ...formData, minimum_stock: parseInt(e.target.value) || 0 })}
                    placeholder="5"
                  />
                </div>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => { setIsModalOpen(false); setSelectedProduct(null); resetForm(); }}>
                Cancel
              </Button>
              <Button type="submit" disabled={isLoadingSubmit}>
                {isLoadingSubmit ? 'Saving...' : selectedProduct ? 'Update Product' : 'Create Product'}
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
              Are you sure you want to delete <span className="font-semibold text-foreground">{productToDelete?.name}</span>?
              This action cannot be undone.
            </p>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => { setIsDeleteModalOpen(false); setProductToDelete(null); }}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={confirmDelete} disabled={deleteMutation.isPending}>
              {deleteMutation.isPending ? 'Deleting...' : 'Delete Product'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};
