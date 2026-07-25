import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { TrendingUp, TrendingDown, DollarSign, Package, ShoppingCart, Wallet } from 'lucide-react';
import { motion } from 'framer-motion';

interface KpiCardProps {
  title: string;
  value: number | string;
  icon: 'revenue' | 'profit' | 'sales' | 'products';
  trend?: number;
}

const icons = {
  revenue: DollarSign,
  profit: Wallet,
  sales: ShoppingCart,
  products: Package,
};

export const KpiCard = ({ title, value, icon, trend }: KpiCardProps) => {
  const Icon = icons[icon];
  const isPositive = trend && trend > 0;

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.2 }}
    >
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">{title}</CardTitle>
          <Icon className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">\</div>
          {trend && (
            <p className="flex items-center gap-1 text-xs">
              {isPositive ? (
                <TrendingUp className="h-3 w-3 text-green-500" />
              ) : (
                <TrendingDown className="h-3 w-3 text-red-500" />
              )}
              <span className={isPositive ? 'text-green-500' : 'text-red-500'}>
                {trend}%
              </span>
              <span className="text-muted-foreground">from last month</span>
            </p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
};
