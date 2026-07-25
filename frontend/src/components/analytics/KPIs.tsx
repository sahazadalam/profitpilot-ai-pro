import { StatCard } from '@/components/shared/StatCard';
import { DollarSign, Package, ShoppingCart, TrendingUp } from 'lucide-react';
import { KPIs as KPIsType } from '@/types/analytics';

interface KPIsProps {
  data: KPIsType;
}

export const KPIs = ({ data }: KPIsProps) => {
  const formatCurrency = (value: number) => {
    return '$' + value.toLocaleString();
  };

  const kpis = [
    {
      title: 'Revenue',
      value: formatCurrency(data?.revenue || 0),
      icon: <DollarSign className="h-4 w-4" />,
      trend: 12.5,
    },
    {
      title: 'Profit',
      value: formatCurrency(data?.profit || 0),
      icon: <TrendingUp className="h-4 w-4" />,
      trend: 8.2,
    },
    {
      title: 'Sales',
      value: (data?.sales || 0).toLocaleString(),
      icon: <ShoppingCart className="h-4 w-4" />,
      trend: 5.3,
    },
    {
      title: 'Products',
      value: (data?.products || 0).toLocaleString(),
      icon: <Package className="h-4 w-4" />,
      trend: 3.1,
    },
  ];

  return (
    <>
      {kpis.map((kpi, index) => (
        <StatCard key={index} {...kpi} />
      ))}
    </>
  );
};
