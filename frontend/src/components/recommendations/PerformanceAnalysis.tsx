import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { motion } from 'framer-motion';
import { BarChart3 } from 'lucide-react';

export const PerformanceAnalysis = ({ data }: any) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BarChart3 className="h-5 w-5" />
          Performance Analysis
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {!data || data.length === 0 ? (
          <p className="text-sm text-muted-foreground">No performance data available</p>
        ) : (
          data.slice(0, 5).map((item: any, index: number) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="space-y-1"
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">{item.product_name}</span>
                <span className="text-sm text-muted-foreground">{item.score}/100</span>
              </div>
              <Progress value={item.score} className="h-2" />
            </motion.div>
          ))
        )}
      </CardContent>
    </Card>
  );
};

