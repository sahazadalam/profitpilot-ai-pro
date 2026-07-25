import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Edit, Trash2, Package, DollarSign, ShoppingBag, Calendar, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { useInventory } from '@/hooks/inventory/useInventory';
import { LoadingScreen } from '@/components/common/LoadingScreen';
import { useState } from 'react';

interface Product {
  id: string;
  name: string;
  sku: string;
  category: string;
  price: number;
  stock: number;
  description?: string;
  supplier?: string;
  createdAt?: string;
  updatedAt?: string;
  status?: 'in-stock' | 'low-stock' | 'out-of-stock' | 'discontinued';
  images?: string[];
}

export const ProductDetails = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { product, isLoading, deleteProduct } = useInventory(id || '');
  const [isDeleting, setIsDeleting] = useState(false);

  if (isLoading) return <LoadingScreen />;
  if (!product) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Package className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-gray-600">Product not found</h2>
          <p className="text-gray-500 mt-2">The product you're looking for doesn't exist.</p>
          <Button className="mt-4" onClick={() => navigate('/inventory')}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Inventory
          </Button>
        </div>
      </div>
    );
  }

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${product.name}"? This action cannot be undone.`)) {
      setIsDeleting(true);
      try {
        await deleteProduct(id || '');
        navigate('/inventory');
      } catch (error) {
        console.error('Failed to delete product:', error);
        alert('Failed to delete product. Please try again.');
        setIsDeleting(false);
      }
    }
  };

  const formatDate = (date?: string) => {
    if (!date) return 'N/A';
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusVariant = (status?: string) => {
    switch (status) {
      case 'in-stock': return 'default';
      case 'low-stock': return 'warning';
      case 'out-of-stock': return 'destructive';
      case 'discontinued': return 'outline';
      default: return 'secondary';
    }
  };

  const getStockStatus = (stock: number) => {
    if (stock <= 0) return 'Out of Stock';
    if (stock < 10) return 'Low Stock';
    if (stock < 50) return 'Running Low';
    return 'In Stock';
  };

  const getStockColor = (stock: number) => {
    if (stock <= 0) return 'text-red-600 bg-red-50 border-red-200';
    if (stock < 10) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    if (stock < 50) return 'text-orange-600 bg-orange-50 border-orange-200';
    return 'text-green-600 bg-green-50 border-green-200';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-4xl mx-auto space-y-6 p-4 md:p-6"
    >
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <Button variant="ghost" onClick={() => navigate('/inventory')} className="w-fit">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Inventory
        </Button>
        
        <div className="flex gap-2">
          <Button 
            onClick={() => navigate(`/inventory/edit/${id}`)}
            className="gap-2"
          >
            <Edit className="h-4 w-4" />
            Edit Product
          </Button>
          <Button 
            variant="destructive" 
            onClick={handleDelete}
            disabled={isDeleting}
            className="gap-2"
          >
            <Trash2 className="h-4 w-4" />
            {isDeleting ? 'Deleting...' : 'Delete'}
          </Button>
        </div>
      </div>

      <Card className="overflow-hidden">
        <CardHeader className="border-b">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <Package className="h-6 w-6 text-primary" />
              </div>
              <div>
                <CardTitle className="text-2xl">{product.name}</CardTitle>
                <p className="text-sm text-muted-foreground">SKU: {product.sku}</p>
              </div>
            </div>
            <Badge variant={getStatusVariant(product.status)} className="capitalize">
              {product.status || 'Active'}
            </Badge>
          </div>
        </CardHeader>

        <CardContent className="p-6 space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="space-y-1">
              <p className="text-sm text-muted-foreground">Category</p>
              <Badge variant="secondary" className="font-medium">
                {product.category || 'Uncategorized'}
              </Badge>
            </div>
            
            <div className="space-y-1">
              <p className="text-sm text-muted-foreground">Price</p>
              <p className="text-xl font-bold text-primary">
                ${product.price?.toFixed(2) || '0.00'}
              </p>
            </div>
            
            <div className="space-y-1">
              <p className="text-sm text-muted-foreground">Stock</p>
              <div className="flex items-center gap-2">
                <span className={`text-xl font-bold px-3 py-1 rounded-lg border ${getStockColor(product.stock || 0)}`}>
                  {product.stock || 0}
                </span>
                <Badge variant="outline" className="text-xs">
                  {getStockStatus(product.stock || 0)}
                </Badge>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4 pt-4 border-t">
            {product.supplier && (
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground">Supplier</p>
                <p className="font-medium">{product.supplier}</p>
              </div>
            )}
            
            {product.createdAt && (
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground">Created</p>
                <p className="font-medium flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  {formatDate(product.createdAt)}
                </p>
              </div>
            )}
            
            {product.updatedAt && (
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground">Last Updated</p>
                <p className="font-medium flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  {formatDate(product.updatedAt)}
                </p>
              </div>
            )}
          </div>

          {product.description && (
            <div className="pt-4 border-t">
              <p className="text-sm text-muted-foreground mb-2">Description</p>
              <p className="text-sm">{product.description}</p>
            </div>
          )}

          <div className="flex flex-wrap gap-3 pt-4 border-t">
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => navigate(`/inventory/stock/${id}`)}
              className="gap-2"
            >
              <ShoppingBag className="h-4 w-4" />
              Manage Stock
            </Button>
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => navigate(`/inventory/pricing/${id}`)}
              className="gap-2"
            >
              <DollarSign className="h-4 w-4" />
              Update Pricing
            </Button>
            {product.stock < 10 && product.stock > 0 && (
              <div className="flex items-center gap-2 text-yellow-600 bg-yellow-50 px-3 py-1 rounded-lg border border-yellow-200">
                <AlertCircle className="h-4 w-4" />
                <span className="text-sm font-medium">Low stock alert</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">Product Details</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div>
              <span className="text-muted-foreground">ID:</span>
              <span className="ml-2 font-mono text-xs">{id}</span>
            </div>
            <div>
              <span className="text-muted-foreground">SKU:</span>
              <span className="ml-2 font-mono text-xs">{product.sku}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default ProductDetails;

