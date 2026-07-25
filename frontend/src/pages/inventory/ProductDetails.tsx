import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Edit, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { useInventory } from '@/hooks/inventory/useInventory';
import { LoadingScreen } from '@/components/common/LoadingScreen';

export const ProductDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { product, isLoading, deleteProduct } = useInventory(id);

  if (isLoading) return <LoadingScreen />;
  if (!product) return <div>Product not found</div>;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-4xl mx-auto space-y-6"
    >
      <div className="flex items-center justify-between">
        <Button
          variant="ghost"
          onClick={() => navigate('/inventory')}
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back
        </Button>

        <div className="flex gap-2">
          <Button
            onClick={() => navigate(`/inventory/edit/${id}`)}
          >
            <Edit className="h-4 w-4 mr-2" />
            Edit
          </Button>

          <Button
            variant="destructive"
            onClick={() => {
              if (window.confirm('Delete this product?')) {
                if (id) {
                  deleteProduct(id);
                }
                navigate('/inventory');
              }
            }}
          >
            <Trash2 className="h-4 w-4 mr-2" />
            Delete
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>{product.name}</CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-sm text-muted-foreground">SKU</p>
              <p className="font-medium">{product.sku}</p>
            </div>

            <div>
              <p className="text-sm text-muted-foreground">Category</p>
              <Badge variant="secondary">
                {product.category}
              </Badge>
            </div>

            <div>
              <p className="text-sm text-muted-foreground">Price</p>
              <p className="font-medium">
                ₹{product.price}
              </p>
            </div>

            <div>
              <p className="text-sm text-muted-foreground">Stock</p>
              <p className="font-medium">
                {product.stock}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};