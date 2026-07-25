import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { motion } from 'framer-motion';
import { Package2 } from 'lucide-react';

export const Bundles = ({ data }: any) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Package2 className="h-5 w-5" />
          Bundle Recommendations
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {!data || data.length === 0 ? (
          <p className="text-sm text-muted-foreground">No bundle recommendations</p>
        ) : (
          data.slice(0, 5).map((item: any, index: number) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="flex items-center justify-between rounded-lg border p-4"
            >
              <div>
                <p className="font-medium">{item.bundle_name}</p>
                <p className="text-sm text-muted-foreground">
                  {item.discount_percentage}% off - 
                </p>
              </div>
              <Badge variant="default"> profit</Badge>
            </motion.div>
          ))
        )}
      </CardContent>
    </Card>
  );
};

