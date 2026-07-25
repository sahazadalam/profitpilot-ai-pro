import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ProductForm } from '@/components/inventory/ProductForm';
import { useInventory } from '@/hooks/inventory/useInventory';

export const AddProduct = () => {
  const navigate = useNavigate();
  const { createProduct } = useInventory();

  const handleSubmit = async (data: any) => {
    await createProduct(data);
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
          <h1 className="text-3xl font-bold">Add Product</h1>
          <p className="text-muted-foreground">Add a new product to inventory</p>
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
          <ProductForm onSubmit={handleSubmit} />
        </CardContent>
      </Card>
    </motion.div>
  );
};

