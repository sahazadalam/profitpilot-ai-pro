import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Clock } from 'lucide-react';
import { motion } from 'framer-motion';

interface RecentSalesProps {
  sales: any[];
}

export const RecentSales = ({ sales }: RecentSalesProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card>
        <CardHeader>
          <CardTitle>Recent Sales</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {sales.length === 0 ? (
              <p className="text-sm text-muted-foreground">No recent sales</p>
            ) : (
              sales.slice(0, 5).map((sale, index) => (
                <motion.div
                  key={sale.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  className="flex items-center justify-between"
                >
                  <div>
                    <p className="text-sm font-medium">{sale.product_name}</p>
                    <p className="text-xs text-muted-foreground">{sale.invoice_number}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium"></p>
                    <p className="text-xs text-muted-foreground">{sale.customer_name || 'Walk-in'}</p>
                  </div>
                </motion.div>
              ))
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

