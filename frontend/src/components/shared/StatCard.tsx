import { Card, CardContent } from '@/components/ui/card';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  trend?: number;
  color?: string;
}

export const StatCard = ({ title, value, icon, trend, color = 'text-primary' }: StatCardProps) => {
  const isPositive = trend && trend > 0;

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.2 }}
    >
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">{title}</p>
              <p className="text-2xl font-bold">{value}</p>
              {trend !== undefined && (
                <div className="flex items-center gap-1 text-xs">
                  {isPositive ? (
                    <TrendingUp className="h-3 w-3 text-green-500" />
                  ) : (
                    <TrendingDown className="h-3 w-3 text-red-500" />
                  )}
                  <span className={isPositive ? 'text-green-500' : 'text-red-500'}>
                    {Math.abs(trend)}%
                  </span>
                  <span className="text-muted-foreground">from last month</span>
                </div>
              )}
            </div>
            <div className={'rounded-lg bg-primary/10 p-3 ' + color}>
              {icon}
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

