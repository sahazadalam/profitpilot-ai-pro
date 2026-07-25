import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { motion } from 'framer-motion';
import { Package, AlertCircle, CheckCircle, Clock } from 'lucide-react';

export const RestockRecommendations = ({ data }: any) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Package className="h-5 w-5" />
          Restock Recommendations
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {data?.length === 0 ? (
          <p className="text-sm text-muted-foreground">No restock recommendations</p>
        ) : (
          data?.slice(0, 5).map((item: any, index: number) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="flex items-center justify-between rounded-lg border p-4"
            >
              <div>
                <p className="font-medium">{item.product_name}</p>
                <p className="text-sm text-muted-foreground">{item.reason}</p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-sm font-medium">Qty: {item.recommended_quantity}</span>
                <Badge variant={item.priority === 'high' ? 'destructive' : 'default'}>
                  {item.priority}
                </Badge>
              </div>
            </motion.div>
          ))
        )}
      </CardContent>
    </Card>
  );
};

