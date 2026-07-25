import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { ProductForm } from '@/components/inventory/ProductForm';
import { useInventory } from '@/hooks/inventory/useInventory';
import { LoadingScreen } from '@/components/common/LoadingScreen';

export const EditProduct = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { product, isLoading, updateProduct } = useInventory(id);

  if (isLoading) return <LoadingScreen />;

  const handleSubmit = async (data: any) => {
    await updateProduct(id, data);
    navigate('/inventory');
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-4xl mx-auto space-y-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Edit Product</h1>
          <p className="text-muted-foreground">Update product information</p>
        </div>
        <Button variant="outline" onClick={() => navigate('/inventory')}>
          Cancel
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Product Details</CardTitle>
        </CardHeader>
        <CardContent>
          <ProductForm initialData={product} onSubmit={handleSubmit} />
        </CardContent>
      </Card>
    </motion.div>
  );
};
