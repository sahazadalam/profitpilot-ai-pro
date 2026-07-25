import { motion } from 'framer-motion';
import { Badge } from '@/components/ui/badge';

interface SalesTableProps {
  sales: any[];
}

export const SalesTable = ({ sales }: SalesTableProps) => {
  return (
    <div className="relative overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b">
            <th className="px-4 py-3 text-left">Invoice</th>
            <th className="px-4 py-3 text-left">Product</th>
            <th className="px-4 py-3 text-left">Customer</th>
            <th className="px-4 py-3 text-left">Qty</th>
            <th className="px-4 py-3 text-left">Amount</th>
            <th className="px-4 py-3 text-left">Date</th>
            <th className="px-4 py-3 text-left">Status</th>
          </tr>
        </thead>
        <tbody>
          {sales.map((sale, index) => (
            <motion.tr
              key={sale.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="border-b hover:bg-muted/50"
            >
              <td className="px-4 py-3 font-medium">{sale.invoice_number}</td>
              <td className="px-4 py-3">{sale.product_name}</td>
              <td className="px-4 py-3">{sale.customer_name || 'N/A'}</td>
              <td className="px-4 py-3">{sale.quantity}</td>
              <td className="px-4 py-3"></td>
              <td className="px-4 py-3">{new Date(sale.sale_date).toLocaleDateString()}</td>
              <td className="px-4 py-3">
                <Badge variant="success">Completed</Badge>
              </td>
            </motion.tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

