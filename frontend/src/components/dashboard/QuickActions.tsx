import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Plus, Package, ShoppingCart, FileText } from 'lucide-react';
import { Link } from 'react-router-dom';

export const QuickActions = () => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        <Link to="/dashboard/inventory/add">
          <Button className="w-full justify-start gap-2">
            <Plus className="h-4 w-4" />
            Add Product
          </Button>
        </Link>
        <Link to="/dashboard/sales">
          <Button className="w-full justify-start gap-2" variant="outline">
            <ShoppingCart className="h-4 w-4" />
            New Sale
          </Button>
        </Link>
        <Link to="/dashboard/inventory">
          <Button className="w-full justify-start gap-2" variant="outline">
            <Package className="h-4 w-4" />
            View Inventory
          </Button>
        </Link>
        <Link to="/dashboard/reports">
          <Button className="w-full justify-start gap-2" variant="outline">
            <FileText className="h-4 w-4" />
            Generate Report
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
};

