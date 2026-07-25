import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { SalesForm } from '@/components/sales/SalesForm';
import { useSales } from '@/hooks/sales/useSales';

export const AddSale = () => {
  const navigate = useNavigate();
  const { createSale } = useSales();

  const handleSubmit = async (data: any) => {
    await createSale(data);
    navigate('/sales');
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
          <h1 className="text-3xl font-bold">New Sale</h1>
          <p className="text-muted-foreground">Create a new sales transaction</p>
        </div>
        <Button variant="outline" onClick={() => navigate('/sales')}>
          Cancel
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Sale Details</CardTitle>
        </CardHeader>
        <CardContent>
          <SalesForm onSubmit={handleSubmit} />
        </CardContent>
      </Card>
    </motion.div>
  );
};
